import sys
import os
import imp
import types
import struct
import marshal

from xdis.magics import PYTHON_MAGIC_INT
from xdis.load import load_module

from xdis.bytecode import Bytecode
from xdis.op_imports import get_opcode_module
from xdis.util import code2num, num2code, COMPILER_FLAG_NAMES
from xdis.cross_dis import format_code_info

from xdis.opcodes import opcode_33, opcode_34
from xdis.opcodes import opcode_35, opcode_36
from xdis.opcodes import opcode_37

from xdis.version import VERSION

def get_opcode(version, is_pypy=False):
    if version == 3.3:
        return opcode_33
    elif version == 3.4:
        return opcode_34
    elif version == 3.5:
        if is_pypy:
            return opcode_35
        else:
            return opcode_36
    elif version == 3.6:
        return opcode_36
    elif version == 3.7:
        return opcode_37
    else:
        raise TypeError("Unsupported Python version %s" % version)

def disassemble_file(filename, outstream=sys.stdout, asm_format="extended"):
    """
    disassemble Python byte-code file (.pyc)

    If given a Python source file (".py") file, we'll
    try to find the corresponding compiled object.
    """
    filename = os.path.realpath(filename)
    mod_name = os.path.basename(filename)
    if mod_name.endswith('.py'):
        mod_name = mod_name[:-3]
    else:
        mod_name = mod_name[:-4]

    version, timestamp, magic_int, co = load_module(mod_name, filename)
    if type(co) == list:
        for con in co:
            disassemble_object(con, timestamp, magic_int,
                               outstream=outstream, asm_format=asm_format)
    else:
        disassemble_object(co, timestamp, magic_int,
                           outstream=outstream, asm_format=asm_format)

def disassemble_object(co, timestamp, magic_int, outstream=sys.stdout, asm_format="extended"):
    """
    disassemble Python object representation to byte-code
    """
    assert isinstance(co, types.CodeType)
    code = co.co_code
    if asm_format == "extended":
        print("# Python %s" % sys.version.split(' ')[0], file=outstream)
        print("# Timestamp: %s" % time.ctime(timestamp), file=outstream)
        print("# Magic: %s" % magic_int, file=outstream)
        print("#" + "-" * 70, file=outstream)
    n = code_info(co, outstream, asm_format=asm_format)
    if asm_format == "extended":
        print("#" + "-" * 70, file=outstream)
    outstream.flush()
    if asm_format == "extended":
        dis_code(co, n, outstream=outstream, asm_format=asm_format)
    else:
        dis_code(co, n, outstream=outstream)

def code_info(co, outstream=sys.stdout, asm_format="extended"):
    """
    Print the code object header
    """
    if asm_format == "extended":
        format_str = '%s -> %s'
    else:
        format_str = '%s, %s'
    if type(co) == list:
        for con in co:
            print(format_str % (con.co_filename, con.co_name), file=outstream)
    else:
        print(format_str % (co.co_filename, co.co_name), file=outstream)
    print("Argument count: %s" % co.co_argcount, file=outstream)
    print("Kw-only arguments: %s" % co.co_kwonlyargcount, file=outstream)
    print("Number of locals: %s" % co.co_nlocals, file=outstream)
    print("Stack size: %s" % co.co_stacksize, file=outstream)
    print("Flags: %s" % pretty_flags(co.co_flags), file=outstream)
    if co.co_consts:
        print("Constants:", file=outstream)
        for i_c in enumerate(co.co_consts):
            print("%4d: %r" % i_c, file=outstream)
    if co.co_names:
        print("Names:", file=outstream)
        for i_n in enumerate(co.co_names):
            print("%4d: %s" % i_n, file=outstream)
    if co.co_varnames:
        print("Variable names:", file=outstream)
        for i_n in enumerate(co.co_varnames):
            print("%4d: %s" % i_n, file=outstream)
    if co.co_freevars:
        print("Free variables:", file=outstream)
        for i_n in enumerate(co.co_freevars):
            print("%4d: %s" % i_n, file=outstream)
    if co.co_cellvars:
        print("Cell variables:", file=outstream)
        for i_n in enumerate(co.co_cellvars):
            print("%4d: %s" % i_n, file=outstream)
    return co.co_argcount

def pretty_flags(flags):
    """
    Munge the flags output by dis.disassemble() into something more readable.
    """
    names = []
    result = ""
    for flag in COMPILER_FLAG_NAMES:
        if flag & flags:
            result += COMPILER_FLAG_NAMES[flag]
            result += " "
    return result.strip()

def dis_code(co, lasti=-1, outstream=sys.stdout, asm_format="extended"):
    """
    Disassemble a code object.

    This function is a port of dis.disassemble from the Python 2.4 version
    of the standard library.
    """
    code = co.co_code
    labels = findlabels(code)
    linestarts = dict(findlinestarts(co))
    n = len(code)
    i = 0
    extended_arg = 0
    free = None
    while i < n:
        have_inner = False
        c = code[i]
        op = code[i]
        if i in linestarts:
            if i > 0:
                print(file=outstream)
            print("%3d" % linestarts[i], file=outstream)
        else:
            print('   ', end=' ', file=outstream)
        if i == lasti: print('-->', end=' ', file=outstream)
        else: print('   ', end=' ', file=outstream)
        if i in labels: print('>>', end=' ', file=outstream)
        else: print('  ', end=' ', file=outstream)
        print(repr(i).rjust(4), end=' ', file=outstream)
        print(opname[op].ljust(20), end=' ', file=outstream)
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = code[i] + code[i + 1] * 256 + extended_arg
            extended_arg = 0
            i = i + 2
            if op == EXTENDED_ARG:
                extended_arg = oparg * 65536
            print(repr(oparg).rjust(5), end=' ', file=outstream)
            if op in hasconst:
                print('(' + repr(co.co_consts[oparg]) + ')', end=' ', file=outstream)
            elif op in hasname:
                print('(' + co.co_names[oparg] + ')', end=' ', file=outstream)
            elif op in hasjrel:
                print('(to ' + repr(i + oparg) + ')', end=' ', file=outstream)
            elif op in haslocal:
                print('(' + co.co_varnames[oparg] + ')', end=' ', file=outstream)
            elif op in hascompare:
                print('(' + cmp_op[oparg] + ')', end=' ', file=outstream)
            elif op in hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars
                print('(' + free[oparg] + ')', end=' ', file=outstream)
            elif op in hasnargs:
                print('(%d positional, %d keyword pair)'
                      % (code[i - 2], code[i - 1]), end=' ', file=outstream)
        print(file=outstream)

def disassemble_string(code, lasti=-1, varnames=None, names=None,
                       constants=None, cells=None,
                       asm_format="extended"):
    labels = findlabels(code)
    n = len(code)
    i = 0
    while i < n:
        have_inner = False
        c = code[i]
        op = ord(c)
        if i == lasti: print('-->', end=' ')
        else: print('   ', end=' ')
        if i in labels: print('>>', end=' ')
        else: print('  ', end=' ')
        print(repr(i).rjust(4), end=' ')
        print(opname[op].ljust(15), end=' ')
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256
            i = i + 2
            print(repr(oparg).rjust(5), end=' ')
            if op in hasconst:
                if constants:
                    print('(' + repr(constants[oparg]) + ')', end=' ')
                else:
                    print('(%d)' % oparg, end=' ')
            elif op in hasname:
                if names is not None:
                    print('(' + names[oparg] + ')', end=' ')
                else:
                    print('(%d)' % oparg, end=' ')
            elif op in hasjrel:
                print('(to ' + repr(i + oparg) + ')', end=' ')
            elif op in haslocal:
                if varnames:
                    print('(' + varnames[oparg] + ')', end=' ')
                else:
                    print('(%d)' % oparg, end=' ')
            elif op in hascompare:
                print('(' + cmp_op[oparg] + ')', end=' ')
            elif op in hasfree:
                if cells:
                    print('(' + cells[oparg] + ')', end=' ')
                else:
                    print('(%d)' % oparg, end=' ')
        print()

disco = disassemble                     # XXX For backwards compatibility

def findlabels(code):
    """Detect all offsets in a byte code which are jump targets.

    Return the list of offsets.

    """
    labels = []
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        op = ord(c)
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256
            i = i + 2
            label = -1
            if op in hasjrel:
                label = i + oparg
            elif op in hasjabs:
                label = oparg
            if label >= 0:
                if label not in labels:
                    labels.append(label)
    return labels

def findlinestarts(code):
    """Find the offsets in a byte code which are start of lines in the source.

    Generate pairs (offset, lineno) as described in Python/compile.c.

    """
    byte_increments = [ord(c) for c in code.co_lnotab[0::2]]
    line_increments = [ord(c) for c in code.co_lnotab[1::2]]

    lastlineno = None
    lineno = code.co_firstlineno
    addr = 0
    for byte_incr, line_incr in zip(byte_increments, line_increments):
        if byte_incr:
            if lineno != lastlineno:
                yield (addr, lineno)
                lastlineno = lineno
            addr += byte_incr
        lineno += line_incr
    if lineno != lastlineno:
        yield (addr, lineno)

def _test():
    """Simple test program to disassemble a file."""
    if sys.argv[1:]:
        if sys.argv[2:]:
            sys.stderr.write("usage: python dis.py [-|file]\n")
            sys.exit(2)
        fn = sys.argv[1]
        if not fn or fn == "-":
            fn = None
    else:
        fn = None
    if fn is None:
        f = sys.stdin
    else:
        f = open(fn)
    source = f.read()
    if fn is not None:
        f.close()
    else:
        fn = "<stdin>"
    code = compile(source, fn, "exec")
    dis(code)

if __name__ == "__main__":
    _test()

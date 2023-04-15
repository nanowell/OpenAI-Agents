#pragma once

#include <iostream>
#include <Windows.h>
#include <TlHelp32.h>

// Function prototypes
DWORD GetProcId(const wchar_t* procName);
uintptr_t GetModuleBaseAddress(DWORD procId, const wchar_t* modName);
uintptr_t FindDynamicAddress(HANDLE hProc, uintptr_t ptr, std::vector<unsigned int> offsets);

// Struct for storing signature data
struct SignatureData {
    const char* pattern;
    const char* mask;
    int additionalOffset;
};

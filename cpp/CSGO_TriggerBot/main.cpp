#include "main.h"

DWORD GetProcId(const wchar_t* procName) {
    DWORD procId = 0;
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    if (hSnap != INVALID_HANDLE_VALUE) {
        PROCESSENTRY32 procEntry;
        procEntry.dwSize = sizeof(procEntry);

        if (Process32First(hSnap, &procEntry)) {
            do {
                if (!_wcsicmp(procEntry.szExeFile, procName)) {
                    procId = procEntry.th32ProcessID;
                    break;
                }
            } while (Process32Next(hSnap, &procEntry));
        }
    }
    CloseHandle(hSnap);
    return procId;
}

uintptr_t GetModuleBaseAddress(DWORD procId, const wchar_t* modName) {
    uintptr_t modBaseAddr = 0;
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, procId);

    if (hSnap != INVALID_HANDLE_VALUE) {
        MODULEENTRY32 modEntry;
        modEntry.dwSize = sizeof(modEntry);

        if (Module32First(hSnap, &modEntry)) {
            do {
                if (!_wcsicmp(modEntry.szModule, modName)) {
                    modBaseAddr = (uintptr_t)modEntry.modBaseAddr;
                    break;
                }
            } while (Module32Next(hSnap, &modEntry));
        }
    }
    CloseHandle(hSnap);
    return modBaseAddr;
}

uintptr_t FindDynamicAddress(HANDLE hProc, uintptr_t ptr, std::vector<unsigned int> offsets) {
    uintptr_t addr = ptr;
    for (unsigned int i = 0; i < offsets.size(); ++i) {
        ReadProcessMemory(hProc, (BYTE*)addr, &addr, sizeof(addr), 0);
        addr += offsets[i];
    }
    return addr;
}

int main() {
    // Get process ID and module base address
    DWORD procId = GetProcId(L"csgo.exe");
    uintptr_t moduleBase = GetModuleBaseAddress(procId, L"client.dll");

    if (!procId || !moduleBase) {
        std::cerr << "Failed to find CS:GO process or module base address." << std::endl;
        return 1;
    }

    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, 0, procId);

    // Define signatures
    SignatureData localPlayerSig = {"\xA1\x00\x00\x00\x00\x85\xC0\x74\x07", "x????xxxx", 1};
    SignatureData entityListSig = {"\xBB\x00\x00\x00\x00\x83\xFF\x01\x0F\x8C\x00\x00\x00\x00\x3B\xF8", "x????xxxxx????xx", 1};
    SignatureData crosshairIDSig = {"\x0F\xB7\x0E\xF3\x0F\x10\x05\x00\x00\x00\x00\xF3\x0F\x11\x80\x00\x00\x00\x00", "xxx??????xxx?????", 4};

    // Get dynamic signatures from game build
    uintptr_t localPlayerOffset = GetDynamicOffset(hProcess, moduleBase, localPlayerSig);
    uintptr_t entityListOffset = GetDynamicOffset(hProcess, moduleBase, entityListSig);
    uintptr_t crosshairIDOffset = GetDynamicOffset(hProcess, moduleBase, crosshairIDSig);

    // Check if offsets are valid
    if (!localPlayerOffset || !entityListOffset || !crosshairIDOffset) {
        std::cerr << "Failed to find dynamic offsets." << std::endl;
        return 1;
    }

    // Main trigger bot loop
    while (true) {
        // Read local player and crosshair ID
        uintptr_t localPlayer = 0;
        ReadProcessMemory(hProcess, (BYTE*)(moduleBase + localPlayerOffset), &localPlayer, sizeof(localPlayer), nullptr);
        int crosshairID = 0;
        ReadProcessMemory(hProcess, (BYTE*)(localPlayer + crosshairIDOffset), &crosshairID, sizeof(crosshairID), nullptr);

        // Check if crosshair is on anenemy
        uintptr_t entity = 0;
        ReadProcessMemory(hProcess, (BYTE*)(moduleBase + entityListOffset + (crosshairID - 1) * 0x10), &entity, sizeof(entity), nullptr);
        int entityTeam = 0;
        ReadProcessMemory(hProcess, (BYTE*)(entity + 0xF0), &entityTeam, sizeof(entityTeam), nullptr);
        int localPlayerTeam = 0;
        ReadProcessMemory(hProcess, (BYTE*)(localPlayer + 0xF0), &localPlayerTeam, sizeof(localPlayerTeam), nullptr);

        // If crosshair is on an enemy, trigger the shot
        if (crosshairID > 0 && crosshairID <= 64 && entityTeam != localPlayerTeam) {
            // Press the left mouse button
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
            Sleep(10); // You can adjust the delay here
            // Release the left mouse button
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
        }

        // Sleep for a short duration to prevent high CPU usage
        Sleep(1);
    }

    CloseHandle(hProcess);
    return 0;
}

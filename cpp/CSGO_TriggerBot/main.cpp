#include "main.h"

TriggerBot::TriggerBot()
    : m_running(false),
      m_processHandle(NULL) {}

TriggerBot::~TriggerBot() {
    stop();
    if (m_processHandle) {
        CloseHandle(m_processHandle);
    }
}

void TriggerBot::start() {
    if (!m_running) {
        m_running = true;
        m_thread = std::thread(&TriggerBot::run, this);
    }
}

void TriggerBot::stop() {
    if (m_running) {
        m_running = false;
        m_thread.join();
    }
}

bool TriggerBot::isRunning() const {
    return m_running;
}

bool TriggerBot::attachToProcess(const std::string& processName) {
    DWORD processId = getProcId(processName);
    if (processId) {
        m_processHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);
        return m_processHandle != NULL;
    }
    return false;
}

void TriggerBot::run() {
    // Replace these with the actual offsets for your game version
    const DWORD localPlayerOffset = 0x0000; // Replace with the actual local player offset
    const DWORD entityListOffset = 0x0000;  // Replace with the actual entity list offset
    const DWORD crosshairIdOffset = 0x0000; // Replace with the actual crosshair ID offset
    const DWORD attackOffset = 0x0000;      // Replace with the actual attack offset
    const DWORD clientDllBase = 0x0000;     // Replace with the actual client DLL base address
    const DWORD forceAttack = 0x1;

    while (m_running) {
        DWORD localPlayer;
        ReadProcessMemory(m_processHandle, (LPCVOID)(clientDllBase + localPlayerOffset), &localPlayer, sizeof(localPlayer), NULL);

        int crosshairId;
        ReadProcessMemory(m_processHandle, (LPCVOID)(localPlayer + crosshairIdOffset), &crosshairId, sizeof(crosshairId), NULL);

        if (crosshairId > 0 && crosshairId <= 64) {
            DWORD entity;
            ReadProcessMemory(m_processHandle, (LPCVOID)(clientDllBase + entityListOffset + (crosshairId - 1) * 0x10), &entity, sizeof(entity), NULL);

            if (entity) {
                WriteProcessMemory(m_processHandle, (LPVOID)(clientDllBase + attackOffset), &forceAttack, sizeof(forceAttack), NULL);
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                forceAttack = 0x0;
                WriteProcessMemory(m_processHandle, (LPVOID)(clientDllBase + attackOffset), &forceAttack, sizeof(forceAttack), NULL);
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
}


bool TriggerBot::checkKeyState(int key) const {
    return GetAsyncKeyState(key) & 0x8000;
}

DWORD TriggerBot::getProcId(const std::string& processName) const {
    DWORD processId = 0;
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    if (hSnapshot != INVALID_HANDLE_VALUE) {
        PROCESSENTRY32 processEntry;
        processEntry.dwSize = sizeof(PROCESSENTRY32);

        if (Process32First(hSnapshot, &processEntry)) {
            do {
                if (!_stricmp(processEntry.szExeFile, processName.c_str())) {
                    processId = processEntry.th32ProcessID;
                    break;
                }
            } while (Process32Next(hSnapshot, &processEntry));
        }
    }
    CloseHandle(hSnapshot);
    return processId;
}

int main() {
    TriggerBot triggerBot;

    if (triggerBot.attachToProcess("csgo.exe")) {
        std::cout << "Attached to csgo.exe\n";
    } else {
        std::cout << "Failed to attach to csgo.exe\n";
        return 1;
    }

    std::cout << "Press F6 to start the trigger bot\n";
    std::cout << "Press F7 to stop the trigger bot\n";

    while (true) {
        if (triggerBot.checkKeyState(KEY_F6)) {
            triggerBot.start();
            std::cout << "Trigger bot started\n";
        } else if (triggerBot.checkKeyState(KEY_F7)) {
            triggerBot.stop();
            std::cout << "Trigger bot stopped\n";
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    return 0;
}

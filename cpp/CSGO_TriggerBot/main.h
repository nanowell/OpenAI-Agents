#pragma once

#include <Windows.h>
#include <iostream>
#include <thread>
#include <chrono>
#include <string>
#include <TlHelp32.h>

constexpr int KEY_F6 = 0x75;
constexpr int KEY_F7 = 0x76;

class TriggerBot {
public:
    TriggerBot();
    ~TriggerBot();
    void start();
    void stop();
    bool isRunning() const;
    bool attachToProcess(const std::string& processName);

private:
    void run();
    bool checkKeyState(int key) const;
    DWORD getProcId(const std::string& processName) const;

    bool m_running;
    std::thread m_thread;
    HANDLE m_processHandle;
};

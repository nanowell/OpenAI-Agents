// File: VpnClient.cpp
#include "VpnClient.h"
#include <cstdio>
#include <string>

VpnClient::VpnClient()
: m_socket(INVALID_SOCKET)
, m_name("VpnClient")
, m_version("1.0")
, m_author("Codex")
, m_description("A sample plugin for VPN Client.")
{ }

VpnClient::~VpnClient()
{
    Finalize();
}

const std::string& VpnClient::GetName() const
{
    return m_name;
}

const std::string& VpnClient::GetVersion() const
{
    return m_version;
}

const std::string& VpnClient::GetAuthor() const
{
    return m_author;
}

const std::string& VpnClient::GetDescription() const
{
    return m_description;
}

bool VpnClient::Initialize()
{
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0)
    {
        printf("WSAStartup failed: %d\n", result);
        return false;
    }

    m_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (m_socket == INVALID_SOCKET)
    {
        printf("Failed to create a socket: %d\n", WSAGetLastError());
        WSACleanup();
        return false;
    }

    char hostname[256];
    if (gethostname(hostname, sizeof(hostname)) == SOCKET_ERROR)
    {
        printf("Failed to get the local hostname: %d\n", WSAGetLastError());
        Finalize();
        return false;
    }

    addrinfo hints = {};
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    addrinfo* addr_result = nullptr;
    if (getaddrinfo(hostname, nullptr, &hints, &addr_result) != 0)
    {
        printf("Failed to get the local IP address: %d\n", WSAGetLastError());
        Finalize();
        return false;
    }

    m_addr.sin_family = AF_INET;
    m_addr.sin_port = htons(80);
    m_addr.sin_addr = reinterpret_cast<sockaddr_in*>(addr_result->ai_addr)->sin_addr;

    freeaddrinfo(addr_result);

    if (connect(m_socket, reinterpret_cast<sockaddr*>(&m_addr), sizeof(m_addr)) == SOCKET_ERROR)
    {
        printf("Failed to connect to the server: %d\n", WSAGetLastError());
        Finalize();
        return false;
    }

    return true;
}

bool VpnClient::Send(const std::string& str)
{
    if (send(m_socket, str.c_str(), static_cast<int>(str.length()), 0) == SOCKET_ERROR)
    {
        printf("Failed to send the string: %d\n", WSAGetLastError());
        return false;
    }

    return true;
}

bool VpnClient::Receive(std::string&str)
{
    char buffer[BUFFER_SIZE];
    int result = recv(m_socket, buffer, BUFFER_SIZE, 0);
    if (result == SOCKET_ERROR)
    {
        printf("Failed to receive the string: %d\n", WSAGetLastError());
        return false;
    }

    str = std::string(buffer, result);
    return true;
}

bool VpnClient::Finalize()
{
    if (closesocket(m_socket) == SOCKET_ERROR)
    {
        printf("Failed to close the socket: %d\n", WSAGetLastError());
        return false;
    }

    if (WSACleanup() == SOCKET_ERROR)
    {
        printf("Failed to clean up Winsock: %d\n", WSAGetLastError());
        return false;
    }

    return true;
}

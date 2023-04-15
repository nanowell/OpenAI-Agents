// File: VpnClient.h
#ifndef VPN_CLIENT_H
#define VPN_CLIENT_H

#include "Plugin.h"
#include <winsock2.h>
#include <ws2tcpip.h>

class VpnClient : public Plugin
{
public:
    VpnClient();
    virtual ~VpnClient();

    const std::string& GetName() const override;
    const std::string& GetVersion() const override;
    const std::string& GetAuthor() const override;
    const std::string& GetDescription() const override;

    bool Initialize() override;
    bool Send(const std::string& str) override;
    bool Receive(std::string& str) override;
    bool Finalize() override;

private:
    SOCKET m_socket;
    struct sockaddr_in m_addr;
    std::string m_name;
    std::string m_version;
    std::string m_author;
    std::string m_description;
};

#endif

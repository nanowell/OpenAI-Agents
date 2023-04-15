#include "VpnClient.h"
#include <iostream>
#include <memory>

int main()
{
    std::unique_ptr<Plugin> plugin = std::make_unique<VpnClient>();

    if (!plugin->Initialize())
    {
        std::cout << "Failed to initialize the plugin." << std::endl;
        return 1;
    }

    if (!plugin->Send("Hello, Server!"))
    {
        std::cout << "Failed to send the string." << std::endl;
        plugin->Finalize();
        return 1;
    }

    std::string response;
    if (!plugin->Receive(response))
    {
        std::cout << "Failed to receive the string." << std::endl;
        plugin->Finalize();
        return 1;
    }

    std::cout << "Server response: " << response << std::endl;

    if (!plugin->Finalize())
    {
        std::cout << "Failed to finalize the plugin." << std::endl;
        return 1;
    }

    return 0;
}

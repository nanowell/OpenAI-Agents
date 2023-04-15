// File: Plugin.h
#ifndef PLUGIN_H
#define PLUGIN_H

#include <string>

// Plugin class
class Plugin
{
public:
    virtual ~Plugin() = default;

    // Plugin information
    virtual const std::string& GetName() const = 0;
    virtual const std::string& GetVersion() const = 0;
    virtual const std::string& GetAuthor() const = 0;
    virtual const std::string& GetDescription() const = 0;

    // Initialization
    virtual bool Initialize() = 0;

    // Send a string to the server
    virtual bool Send(const std::string& str) = 0;

    // Receive a string from the server
    virtual bool Receive(std::string& str) = 0;

    // Finalization
    virtual bool Finalize() = 0;
};

#endif

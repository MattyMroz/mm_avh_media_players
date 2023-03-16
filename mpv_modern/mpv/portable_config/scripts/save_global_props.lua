--[[

SOURCE_ https://github.com/zenwarr/mpv-config/blob/master/scripts/remember-props.lua
COMMIT_ 20220811 03cfc0e39682a73d9d24a6e01a3c02716a019d1d

Rejestrowanie zmian globalnych właściwości, umożliwia przywrócenie ich przy następnym uruchomieniu programu. Dane są zapisywane w pliku saved-props.json
(Opcja --save-position-on-quit zapisuje atrybuty oparte na konkretnym pliku, nie powinna kolidować z atrybutami zapisanymi przez --watch-later-options)

Przykład zapisania danych w pliku input.conf (wyczyszczenie zapisanych danych) :
CTRL+r script-message-to save_global_props clean_data

]]--

local mp = require("mp")
local options = require("mp.options")
local utils = require("mp.utils")


local function split(inputstr, sep)
    local result = {}

    for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
        table.insert(result, str)
    end

    return result
end


local script_options = {
    props     = "volume,mute,speed",   -- Dostosuj właściwości do zapisu
    cache_dir = "~~/"                  -- Ścieżka do pliku podręcznego/cache
}
options.read_options(script_options)
script_options.props = split(script_options.props, ",")


local data_file_path = (mp.command_native({'expand-path', script_options.cache_dir .. "saved-props.json"}))


local function read_data_file()
    local json_file = io.open(data_file_path, 'a+')
    local result = utils.parse_json(json_file:read("*all"))
    if result == nil then
        result = {}
    end
    json_file:close()

    return result
end


local saved_data = read_data_file()


local function save_data_file()
    local file = io.open(data_file_path, 'w+')
    if file == nil then
        return
    end

    local content, ret = utils.format_json(saved_data)
    if ret ~= error and content ~= nil then
        file:write(content)
    end

    file:close()
end


local function clean_data_file()
    local file = io.open(data_file_path, 'w+')
    if file == nil then
        return
    end

    local content = ''
    file:write(content)

    file:close()
    mp.osd_message("Już wyczyszczone rekordy", 1)
end


local function init()
    for _, prop_name in ipairs(script_options.props) do
        local saved_value = saved_data[prop_name]
        if saved_value ~= nil then
            mp.set_property_native(prop_name, saved_value)
        end

        mp.observe_property(prop_name, "native", function(_, prop_value)
            saved_data[prop_name] = mp.get_property_native(prop_name)
            save_data_file()
        end)
    end
end


init()

mp.register_script_message("clean_data", clean_data_file)

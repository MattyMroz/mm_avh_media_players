--[[

ŹRÓDŁO_ https://github.com/zenwarr/mpv-config/blob/master/scripts/remember-props.lua
COMMIT_ 20220811 03cfc0e39682a73d9d24a6e01a3c02716a019d1d

Zapisuje zmiany globalnych właściwości, umożliwiając ich przywrócenie przy następnym uruchomieniu programu, dane są zapisywane w odpowiednim pliku saved-props.json
(opcja --save-position-on-quit zapisuje właściwości specyficzne dla danego pliku, nie powinna kolidować z właściwościami zapisywanymi przez --watch-later-options)

Przykład wprowadzenia do input.conf (usuwa zapisane dane):
CTRL+r script-message-to save_global_props clean_data

]]

local mp = require("mp")
local options = require("mp.options")
local utils = require("mp.utils")

local script_options = {
	save_mode = 1,                     -- <0|1|2> Czas zapisu właściwości. Nie zapisuje/Przed normalnym zamknięciem/Na podstawie zmiany właściwości
	props     = "volume,mute,speed",   -- Własne właściwości do zapisu
	cache_dir = "~~/"                  -- Ścieżka do pliku cache
}
options.read_options(script_options)

if script_options.save_mode == 0 then
	mp.msg.info("Funkcja zapisu globalnych właściwości jest wyłączona")
	return
end

local function split(inputstr, sep)
	local result = {}
	for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
		table.insert(result, str)
	end
	return result
end

script_options.props = split(script_options.props, ",")

local cleaned = false
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
	if cleaned then
		mp.msg.verbose("Zapis zatrzymany z powodu czyszczenia zapisanych właściwości")
		return
	end
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
	cleaned = true
	mp.osd_message("Wyczyszczono zapisane właściwości\nZalecany restart mpv", 2)
end

local function init()
	for _, prop_name in ipairs(script_options.props) do
		local saved_value = saved_data[prop_name]
		if saved_value ~= nil then
			mp.set_property_native(prop_name, saved_value)
		end
		if script_options.save_mode == 2 then
			mp.observe_property(prop_name, "native", function(_, prop_value)
				saved_data[prop_name] = mp.get_property_native(prop_name)
				save_data_file()
			end)
		end
	end
end

init()

if script_options.save_mode == 1 then
	mp.register_event("shutdown", function()
		for _, prop_name in ipairs(script_options.props) do
			saved_data[prop_name] = mp.get_property_native(prop_name)
			save_data_file()
		end
	end)
end

mp.register_script_message("clean_data", clean_data_file)

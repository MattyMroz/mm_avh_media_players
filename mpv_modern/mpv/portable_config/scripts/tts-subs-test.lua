local utils = require 'mp.utils'

local function exec(args)
    local ret = utils.subprocess({
        args = args
    })
    return ret.status, ret.stdout, ret
end

local last_text = ""
local enabled = false

local function say(text)
    local _, _, winapi = utils.win_get_function_ptrs()
    local hMm = winapi.mscreate("SAPI.SpVoice")
    winapi.mssetvoice(hMm, winapi.voice_nametoid("Polish"))
    winapi.msspeak(hMm, text, 1)
    winapi.msclose(hMm)
end

mp.observe_property("sub-text", "string", function(prop, txt)
    if enabled and txt ~= nil and txt ~= last_text then
        last_text = txt
        say(txt)
    end
end)

mp.add_key_binding("Ctrl+x", "toggle-tts-subs", function()
    enabled = not enabled
    mp.osd_message("Subtitle TTS mode: " .. utils.to_string(enabled))
end)

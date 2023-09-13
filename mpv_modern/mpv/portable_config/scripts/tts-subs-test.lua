-- local utils = require 'mp.utils'

-- local function exec(args)
--     local ret = utils.subprocess({
--         args = args
--     })
--     return ret.status, ret.stdout, ret
-- end

-- local tts_rate = 5
-- local tts_volume = 65
-- local enabled = false
-- mp.add_key_binding("Ctrl+x", "toggle-tts", function()
--     enabled = not enabled
--     mp.osd_message("Tryb TTS: " .. tostring(enabled))
-- end)

-- mp.observe_property("sub-text", "string", function(prop, txt)
--     if enabled and txt then
--         local tts_command = string.format(
--             'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Rate = %d; $speak.Volume = %d; $speak.SelectVoice(\'Vocalizer Expressive Zosia Harpo 22kHz\'); $speak.Speak(\'%s\')',
--             tts_rate, tts_volume, txt)
--         local status, stdout = exec({"powershell", "-Command", tts_command})

--         mp.osd_message("Odczytywany tekst: " .. txt)
--     end
-- end)

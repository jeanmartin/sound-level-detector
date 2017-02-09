require 'pry'

God.watch do |w|
  w.name = 'detect_sound_level'
  w.start = 'python3 /home/pi/sound/detect_sound_level.py'
  w.keepalive

  # start if process is not running
  w.transition(:up, :start) do |on|
    on.condition(:process_exits) do |c|
      c.notify = 'cthulhu'
    end
  end
end

God.contact(:slack) do |c|
  c.name = 'cthulhu'
  c.url = 'https://hooks.slack.com/services/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'
end

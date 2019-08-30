#!/usr/bin/tmux source 
split-window -h -c "#{pane_current_path}"
send-keys "tsc --watch" C-m
split-window -v -c "#{pane_current_path}"
send-keys "make watch" C-m
split-window -v -c "#{pane_current_path}"
send-keys "cd dist; python3 -m http.server 8081" C-m
select-layout main-vertical
select-pane -L
resize-pane -x 100

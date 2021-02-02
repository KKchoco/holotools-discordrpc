# holotools-discordrpc
An ugly attempt to make Discord Rich Presence for https://hololive.jetri.co/

you need to add your youtube api key to line 55 to get it to work
holotools-rpc.js needs to be installed using Tampermonkey or alternative
list.json contains youtube channel ids + viewed names matches

TODO: some kind of heartbeat from browser to http server to tell script that tab is still open, cause if you close holotools tab or browser without closing all videos rich presense will stay active

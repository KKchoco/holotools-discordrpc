// ==UserScript==
// @name         HoloTools Discord Rich Presence
// @namespace    https://
// @version      0.1
// @description  test
// @author       test
// @license      MIT
// @run-at document-end
// @match        https://hololive.jetri.co/*
// @grant        GM_xmlhttpRequest
// @grant window.onurlchange
// ==/UserScript==
console.log("HoloTools Discord RPC Userscript hooked!");
if (window.onurlchange === null) {
    window.addEventListener("urlchange", (info) => {
        GM_xmlhttpRequest({
            method: "POST",
            url: "http://127.0.0.1:6553/setRP",
            data: JSON.stringify({
                'url': window.document.URL
            }),
            headers: {
                "Content-Type": "application/json"
            },
            onload: function(response) {
                console.log(response.responseText);
            },
            onerror: function(reponse) {
                //alert('error');
                console.log("error: ", reponse);
            }
        });
    }, 2000);
};
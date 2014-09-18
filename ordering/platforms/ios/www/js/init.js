/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

var app = {
    // Application Constructor
    menu: null,
    
    initialize: function() {
        this.bindEvents();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicitly call 'app.receivedEvent(...);'
    onDeviceReady: function() {
        app.receivedEvent('deviceready');
    },
    
    getMenu: function() {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://localhost:5000/menu", false);
        xhr.send();

        if(xhr.status != 200) {
            if(xhr.status != 404) {
                document.getElementById("menu-list").innerHTML = "<p>Error when loading menu list</p>";
            }
            error_msg = JSON.parse(xhr.responseText);
            document.getElementById("menu-list").innerHTML = error_msg.message;
        }
        var jsonResponse = JSON.parse(xhr.responseText);
        menu_template = app.constructMenu(jsonResponse, HOST_NAME+'/order', 'post');
        document.getElementById("menu-list").innerHTML = menu_template;
    },
    
    constructMenu: function(menu, url, method, id) {
        // Setup default values
        url = typeof url !== "undefined" ? url : HOST_NAME;
        method = typeof method !== "undefined" ? method : 'get';
        id = typeof id !== "undefined" ? id : 'menu-form';
        
        template = "<form action=" + url + " method=" + method + " id=" + id + ">";

        // Construct the menu
        var menuHtml = "";
        for(var key in menu) {
            if(menu.hasOwnProperty(key)) {
                menuHtml += "<h3><em class='bold'>" + key + "</em></h3>";
                for(var i = 0; i < menu[key].length; ++i) {
                    
                    menuHtml += "<input type='checkbox' name='menu' " +
                            "value=" + menu[key][i].replace(/ /g, '-') + ">" +
                            menu[key][i] + "</span><br>";
                    
                }
            }
        }
        userInfo = StringUtils.string_inject(USER_INFO, [id]);
        template += menuHtml + userInfo +
                "<div><input type='submit' value='Submit'><div></form>";
        
        return template;
    },
    
    // Update DOM on a Received Event
    receivedEvent: function(id) {
        app.getMenu();
        console.log('Received Event: ' + id);
    }
};
function update_values() {
            $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
            $.getJSON($SCRIPT_ROOT+"_update_live_values",
                function(data) {
                    $("#A1").text(data.A1)
                    $("#A2").text(data.A2)
                    $("#A3").text(data.A3)
                    $("#A4").text(data.A4)
                });
        }
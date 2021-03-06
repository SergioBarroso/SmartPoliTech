# -*- coding: utf-8 -*-
from zato.server.service import Service


class MapBox(Service):

    def handle(self):
        self.response.payload = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
        integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"
        integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous">
        </script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css"
        integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
        crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"
        integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw=="
        crossorigin=""></script>
    <script src="http://158.49.112.127:11223/sidebar_leaflet_js"></script>
    <link rel="stylesheet" href="http://158.49.112.127:11223/sidebar_leaflet_css" />
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
    <script
        src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-omnivore/v0.3.1/leaflet-omnivore.min.js'></script>
    <script type="text/javascript" src="http://158.49.112.127:11223/zlibjs"></script>
    <style>
        #mapid {
            position: absolute;
            width: 100%;
            top: 0;
            /* The height of the header */
            bottom: 0;
            left: 0;
        }

        .margin-left-1rem {
            margin-left: 1rem;
        }

        .padding-left-1rem {
            padding-left: 1rem;
        }

        .padding-left-3rem {
            padding-left: 3rem;
        }
    </style>
    <title>Map Box Testing</title>
</head>

<body>
    <div id='mapid'></div>

    <div id="sidebar" class="sidebar collapsed ">
        <!-- Nav tabs -->
        <div class="sidebar-tabs">
            <ul role="tablist">
                <li><a href="#home" role="tab"><i class="fa fa-bars"></i></a></li>
                <li><a href="#search" role="tab"><i class="fa fa-search"></i></a></li>
            </ul>

            <ul role="tablist">
                <li><a href="#settings" role="tab"><i class="fa fa-gear"></i></a></li>
            </ul>
        </div>

        <!-- Tab panes -->
        <div class="sidebar-content">
            <div class="sidebar-pane" id="home">
                <h1 class="sidebar-header">
                    Filtros
                    <span class="sidebar-close"><i class="fa fa-caret-right"></i></span>
                </h1>
                <br>
                <div style="display: block">
                    <ul style=" list-style-type: none; margin: 0 0 3px 0;">
                        <li>
                            <h2>Planta</h2>
                        </li>
                        <li style="margin: 5 0 5px 0;"><select id="select" onchange="( function(){
                            selectedFloor = $('#select').val();
                            processNodes(nodes);
                        })();return false;">
                                <option value="0">Planta 0</option>
                                <option value="1">Planta 1</option>
                                <option value="2">Planta 2</option>
                                <option value="-1">Planta S1</option>
                            </select></li>
                        <li>
                            <h2>Tipo de elemento</h2>
                        </li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="People" value=1 checked
                                    onclick="(function() {
                            People *= -1;
                            processNodes(nodes);
                        })()">
                                Personas </label> </listyle="margin: 0 0 3px 0;">
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="Devices" value=1 checked
                                    onclick="(function() {
                            Devices *= -1;
                            processNodes(nodes);
                        })()">
                                Dispositivos </label></li>
                        <li>
                            <h2>Áreas </h2>
                        </li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="aula" onclick="(function() {
                            Aula *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Aula </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="lab" onclick="(function() {
                            Lab *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Laboratorio </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="despacho" onclick="(function() {
                            Despacho *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Despacho </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="comun" onclick="(function() {
                            Comun *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Pasillo/Común </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="cuarto" onclick="(function() {
                            Cuarto *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Cuarto </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="aseo" onclick="(function() {
                            Aseo *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Aseo </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="sala" onclick="(function() {
                            Sala *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Sala </label></li>
                    </ul>
                </div>
            </div>
            <div class="sidebar-pane" id="search">
                <h1 class="sidebar-header">
                    Consultas
                    <span class="sidebar-close"><i class="fa fa-caret-right"></i></span>
                </h1>
                <br>
                <input type="text" placeholder="Search..">
                <button onclick="sendQuery()"> Buscar </button>
            </div>
            <div class="sidebar-pane" id="settings">
                <h1 class="sidebar-header">Settings<span class="sidebar-close"><i class="fa fa-caret-right"></i></span>
                </h1>
            </div>
        </div>
    </div>


    <script>
        //Creación del objeto mapa
        var map = L.map('mapid', { zoomDelta: 0.5, zoomSnap: 0.5 }).setView([39.47841096088879, -6.340684443712235], 20);


        var streets = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZmFoYW5pIiwiYSI6ImNqMTZiYm4xMjAyYjEzMnFxdmxnd2V3cHkifQ.-8Hau4tMxMiiSF-9D5AAYA', { maxZoom: 25 }).addTo(map);
        var sidebar = L.control.sidebar('sidebar').addTo(map);
        var Areas = []
        map.on('moveend', function onDragEnd(s) {
            console.log(map.getZoom());
            

            let Area_Visible = map.getBounds();
            var is_new_area = true;

            for (var i = 0; i < Areas.length; i++){
                if (Areas[i].contains(Area_Visible)) { 
                    is_new_area = false; 
                    break;
                }
            }
            if (is_new_area){
                Areas = Areas.filter(area => !Area_Visible.contains(area));
                Areas.push(Area_Visible)
                queryNeo4j();
            }

            if (nodes != null) {
                processNodes(nodes);
            }

        });

        var layers = [];
        var layersIds = [];

        var nodes = [];
        

        var selectedFloor = parseInt($('#select').val());

        var People = $('#People:checked').val() == "1" ? 1 : -1;;
        var Devices = $('#Devices:checked').val() == "1" ? 1 : -1;;

        var Aseo = $('#aseo:checked').val() == "1" ? 1 : -1;
        var Aula = $('#aula:checked').val() == "1" ? 1 : -1;
        var Lab = $('#lab:checked').val() == "1" ? 1 : -1;
        var Comun = $('#comun:checked').val() == "1" ? 1 : -1;
        var Despacho = $('#despacho:checked').val() == "1" ? 1 : -1;
        var Sala = $('#sala:checked').val() == "1" ? 1 : -1;
        var Cuarto = $('#cuarto:checked').val() == "1" ? 1 : -1;

        queryNeo4j();





        function processNodes(nodes) {

            defineDiff();

            // Collect the ids of the building nodes that matches the spatial query
            let matchedNodes = [];
            let nodesToDraw = [];
            nodes.forEach(function (node) {

                if (Devices == -1 && node.graph.nodes[0].labels[0] == "Device") { return; }
                if (People == -1 && node.graph.nodes[0].labels[0] == "People") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Aseo == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "aseo") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Aula == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "aula") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Lab == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "laboratorio") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Comun == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "comun") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Despacho == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "despacho") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Sala == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "sala") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Cuarto == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "cuarto") { return; }
                if (node.graph.nodes[0].properties.id  == undefined) { return; }

                //TODO: revisar esta condición 
                // Add it is between the zoom
                if (node.graph.nodes[0].properties.min_zoom <= map.getZoom() && map.getZoom() <= node.graph.nodes[0].properties.max_zoom /*|| map.getZoom() < 20*/ || map.getZoom() > 50) {

                    // If it is a floor, add only the selected ones
                    if (node.graph.nodes[0].labels[0] == "Floor") {
                        if (node.graph.nodes[0].properties.id  == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id  == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id  == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id  == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id  == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id  == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id  == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id  == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id );
                            nodesToDraw[node.graph.nodes[0].properties.id ] = node.graph.nodes[0].properties;
                        }

                    } else if (node.graph.nodes[0].labels[0] == "Building") {
                        matchedNodes.push(node.graph.nodes[0].properties.id );
                        nodesToDraw[node.graph.nodes[0].properties.id ] = node.graph.nodes[0].properties;
                    }
                    else if (node.graph.nodes[0].labels[0] == "Alerts") {
                        matchedNodes.push(node.graph.nodes[0].properties.id );
                        nodesToDraw[node.graph.nodes[0].properties.id ] = node.graph.nodes[0].properties;

                    } else if (selectedFloor == 0) {
                        if (node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id );
                            nodesToDraw[node.graph.nodes[0].properties.id ] = node.graph.nodes[0].properties;
                        }
                    } else if (selectedFloor == 1) {
                        if (node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id );
                            nodesToDraw[node.graph.nodes[0].properties.id ] = node.graph.nodes[0].properties;
                        }
                    } else if (selectedFloor == 2) {
                        if (node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id );
                            nodesToDraw[node.graph.nodes[0].properties.id ] = node.graph.nodes[0].properties;
                        }
                    } else if (selectedFloor == -1) {
                        if (node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id .substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id );
                            nodesToDraw[node.graph.nodes[0].properties.id ] = node.graph.nodes[0].properties;
                        }
                    }
                }
            });


            let nodesToRemove = layersIds.diff(matchedNodes);
            removeNodes(nodesToRemove);

            matchedNodes.forEach(function (nodeToAdd) {


                function style(feature) {
                    return {
                        color: feature.style.fill ? feature.style.fill : '#3388ff',
                        fillOpacity: feature.style.fill_opacity ? feature.style.fill_opacity : 0.4,
                        width: 2

                    };
                }
                function onEachFeature(feature, layer) {

                    let bindText = "";

                    if (nodesToDraw[nodeToAdd].dataSource) {
                        bindText = bindText + "" + nodesToDraw[nodeToAdd].dataSource + "<br> <a href='" + $(nodesToDraw[nodeToAdd].dataSource)[0].src + "' target='_blank'>Abrir en ventana</a>";
                    }
                    else if (feature.properties && feature.properties.name)
                        //bindText = bindText + "" + feature.properties.name + "<br>" + nodesToDraw[nodeToAdd].id;
                        bindText = bindText + "" + nodesToDraw[nodeToAdd].name + "<br> " + nodesToDraw[nodeToAdd].id;

                    else
                        bindText = ""
                    layer.bindPopup(bindText);

                }

                // add it if the node doesn't exist in the map
                if (!layers[nodeToAdd]) {

                    // add it if the node has the geojson property and the geojson is valid json
                    if (nodesToDraw[nodeToAdd].geojson != undefined && isJson(nodesToDraw[nodeToAdd].geojson)) {
                        layersIds.push(nodeToAdd);


                        if (nodesToDraw[nodeToAdd].Alerts) {

                            fetch(nodesToDraw[nodeToAdd].Alerts).then(function (response) {
                                return response.json();
                            }).then(response => {
                                let json = response;
                                if (json == "aviso") {

                                    layers[nodeToAdd] = L.geoJSON(JSON.parse(nodesToDraw[nodeToAdd].geojson),
                                        {
                                            pointToLayer: function (feature, latlng) {
                                                let icon = L.icon({ iconUrl: nodesToDraw[nodeToAdd].Alertsimg });
                                                return marker = L.marker(latlng, { icon: icon })

                                            }, style: style,
                                            onEachFeature: onEachFeature

                                        });
                                    layers[nodeToAdd].addTo(map);
                                }
                            });

                        } else {

                            layers[nodeToAdd] = L.geoJSON(JSON.parse(nodesToDraw[nodeToAdd].geojson),
                                {
                                    pointToLayer: function (feature, latlng) {
                                        if (nodesToDraw[nodeToAdd].img) {
                                            let icon = L.icon({ iconUrl: nodesToDraw[nodeToAdd].img });
                                            return L.marker(latlng, { icon: icon });
                                        }

                                    },
                                    style: style,
                                    onEachFeature: onEachFeature
                                });

                            layers[nodeToAdd].addTo(map);
                        }
                    }
                }
            });
            //console.log("Terminado")

        }


        function removeNodes(nodesToRemove) {
            //Removen nodes from the map.
            nodesToRemove.forEach(function (nodeToRemove) {
                if (layers[nodeToRemove]) {
                    map.removeLayer(layers[nodeToRemove]);
                }
                delete layers[nodeToRemove];

                let index = layersIds.indexOf(nodeToRemove);
                if (index > -1) {
                    layersIds.splice(index, 1);
                }
            });

        }

        function queryNeo4j() {
            
          
            

            $.ajax({
                url: "http://158.49.112.127:11223/neozip",
                headers: {
                    "Cache-Control": "public",
                },
                type: "POST",
                data: JSON.stringify({ 
                    "query": [ "" + map.getBounds().getNorthWest().lng+" "+map.getBounds().getNorthWest().lat + "" ,
                    "" + map.getBounds().getNorthEast().lng+" "+map.getBounds().getNorthEast().lat + "" ,
                    "" + map.getBounds().getSouthEast().lng+" "+map.getBounds().getSouthEast().lat + "" ,
                    "" + map.getBounds().getSouthWest().lng+" "+map.getBounds().getSouthWest().lat + "" ,
                    "" + map.getBounds().getNorthWest().lng+" "+map.getBounds().getNorthWest().lat + "" 
                    ]
                }),
                error: function (err) {
                    alert("error");
                },
                success: function (res) {
                    res = atob(res)
                    var data = new Array(res.length);
                    for (i = 0, il = res.length; i < il; ++i) {
                        data[i] = res.charCodeAt(i);
                    }

                    var inflate = new Zlib.Inflate(data);
                    var decompress = inflate.decompress();
                    res = JSON.parse(new TextDecoder("utf-8").decode(decompress))
                    if (res.results) {
                        new_nodes = res.results[0].data;
                        
                        new_nodes.forEach(node => { 
                            not_found = true;
                            for (var i = 0; i < nodes.length; i++) {
                                if (nodes[i].graph.nodes[0].properties.id == node.graph.nodes[0].properties.id) {
                                    not_found = false;
                                    return;
                                }
                            }
                            nodes.push( node) ; 
                        });
                        
                        console.log(nodes);
                        processNodes(nodes);
                    }
                }
            });
        }

        function isJson(item) {
            //check if object can be parsed to json.
            item = typeof item !== "string"
                ? JSON.stringify(item)
                : item;

            try {
                item = JSON.parse(item);
            } catch (e) {
                return false;
            }

            if (typeof item === "object" && item !== null) {
                return true;
            }

            return false;
        }

        function defineDiff() {
            // Define diff function in arrays
            Array.prototype.diff = function (a) {
                return this.filter(function (i) {
                    return a.indexOf(i) === -1;
                });
            };
        }

    </script>

</body>

</html>
        """

        self.response.content_type = 'text/html; charset=utf-8'

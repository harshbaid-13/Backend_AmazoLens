from folium import Marker
from folium.plugins import MarkerCluster
from jinja2 import Template
import folium
import datetime
from folium import plugins
import pandas as pd
import numpy as np
import json
class MarkerWithProps(Marker):
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var {{this.get_name()}} = L.marker(
            [{{this.location[0]}}, {{this.location[1]}}],
            {
                icon: new L.Icon.Default(),
                {%- if this.draggable %}
                draggable: true,
                autoPan: true,
                {%- endif %}
                {%- if this.props %}
                props : {{ this.props }} 
                {%- endif %}
                }
            )
            .addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)
    def __init__(self, location, popup=None, tooltip=None, icon=None,
                 draggable=False, props = None ):
        super(MarkerWithProps, self).__init__(location=location,popup=popup,tooltip=tooltip,icon=icon,draggable=draggable)
        self.props = json.loads(json.dumps(props))
  

icon_create_function_gmv = """
   function(cluster) {
    var markers = cluster.getAllChildMarkers();
    var sum = 0;
    for (var i = 0; i < markers.length; i++) {
        sum += markers[i].options.props.population;
    }
    var avg = (sum).toFixed(0);
    
var c = ' marker-cluster-';

if (avg > 5000) {
    c += 'large';
} else if (avg > 1000) {
    c += 'medium';
} else {
    c += 'small';
}

return new L.DivIcon({ html: '<div><span>' + avg  + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });

}
"""

icon_create_function_gmv2 = """
   function(cluster) {
    var markers = cluster.getAllChildMarkers();
    var sum = 0;
    for (var i = 0; i < markers.length; i++) {
        sum += markers[i].options.props.population;
    }
    
    var displayValue = '';
    if (sum >= 100000) {
        displayValue = (sum / 100000).toFixed(1) + 'L';
        displayValue=displayValue.toString()
    } else {
        displayValue = sum.toFixed(0).toString();
    }

    var c = ' marker-cluster-';

    if (sum > 1000000) {
        c += 'large';
    } else if (sum > 50000) {
        c += 'medium';
    } else {
        c += 'small';
    }

    return new L.DivIcon({ 
        html: '<div><span>' + displayValue + '</span></div>', 
        className: 'marker-cluster' + c, 
        iconSize: new L.Point(40, 40) 
    });
}
"""

icon_create_function_aov = """
   function(cluster) {
    var markers = cluster.getAllChildMarkers();
    var sum = 0;
    var sum2=0;
    for (var i = 0; i < markers.length; i++) {
        sum += markers[i].options.props.population;
        sum2+=markers[i].options.props.pop2;
    }
    var avg = (sum/sum2).toFixed(1);
    
var c = ' marker-cluster-';

if (avg > 500) {
    c += 'large';
} else if (avg > 100) {
    c += 'medium';
} else {
    c += 'small';
}

return new L.DivIcon({ html: '<div><span>' + avg + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });

}
"""



def make_folium_map(sales):
    
    agg_data=sales.groupby(['city','latitude','longitude'])[['customer_id','order_id','total_weighted_landing_price','product_id']].agg(
        {"customer_id":'nunique',"order_id":'nunique','total_weighted_landing_price':sum,"product_id":'nunique'})
    agg_data=agg_data.reset_index()
    
    latitude = 28
    longitude = 77
    ind_map = folium.Map(location=[latitude, longitude], zoom_start=5, 
    tiles = 'OpenStreetMap')
    # folium.TileLayer(
    # tiles = f"https://api.mapbox.com/styles/v1/planemad/ckf4xcet7231819mm2e8njlca/tiles/512/{{z}}/{{x}}/{{y}}@2x?access_token=pk.eyJ1IjoiYXJ5YW5hMjQiLCJhIjoiY205bWp6aWF4MGRrcTJtcXUyanVoN2s4ZCJ9.coUrqISCH0zp4Lu2q_SpCg",
    # attr="Mapbox",name = 'Choose any metric',overlay=True,show=True, control=False
    #           ).add_to(ind_map)
    
    incidents_gmv = plugins.MarkerCluster(name='GMV',icon_create_function=icon_create_function_gmv2,
                                                           overlay=False).add_to(ind_map)
    for lat, lng, label,metric in zip(agg_data.latitude, agg_data.longitude,
                                                agg_data.city,agg_data.total_weighted_landing_price.astype(int)):
                        MarkerWithProps(
                            location=[lat, lng],
                            icon=folium.DivIcon(html=f"""
                <div> <svg>
                <circle cx="17" cy="17" r="17" fill="#9FCC4C" opacity=".5"/>
                <circle cx="17" cy="17" r="13" fill="#9FCC4C" opacity=".5"/>
                <text x="5.5%" y="15%" text-anchor="middle">{str(metric)}</text>
                </svg></div>"""),
                            popup=label,
                            props={ 'population': metric},
                        ).add_to(incidents_gmv)
    ind_map.add_child(incidents_gmv)

    # users
    incidents_users = plugins.MarkerCluster(name='Customers',icon_create_function=icon_create_function_gmv,
                                                           overlay=False).add_to(ind_map)
    for lat, lng, label,metric in zip(agg_data.latitude, agg_data.longitude,
                                                agg_data.city,agg_data.customer_id.astype(int)):
                        MarkerWithProps(
                            location=[lat, lng],
                            icon=folium.DivIcon(html=f"""
                <div> <svg>
                <circle cx="17" cy="17" r="17" fill="#9FCC4C" opacity=".5"/>
                <circle cx="17" cy="17" r="13" fill="#9FCC4C" opacity=".5"/>
                <text x="5.5%" y="15%" text-anchor="middle">{str(metric)}</text>
                </svg></div>"""),
                            popup=label,
                            props={ 'population': metric},
                        ).add_to(incidents_users)
    ind_map.add_child(incidents_users)
    
    
    # AOV 
    incidents_aov = plugins.MarkerCluster(name='Avg. Order Value (AOV)',
                                           icon_create_function=icon_create_function_aov,
                                           overlay=False).add_to(ind_map)
    
    for lat, lng, label,metric, metric2 in zip(agg_data.latitude, agg_data.longitude,agg_data.city,agg_data.total_weighted_landing_price,agg_data.customer_id.astype(int) ):
        MarkerWithProps(
            location=[lat, lng],
            icon=folium.DivIcon(html=f"""
        <div> <svg>
        <circle cx="17" cy="17" r="17" fill="#9FCC4C" opacity=".5"/>
        <circle cx="17" cy="17" r="13" fill="#9FCC4C" opacity=".5"/>
        <text x="5.5%" y="15%" text-anchor="middle">{str(round(metric/metric2,2))}</text>
        </svg></div>"""),
            popup=label,
            props={ 'population': metric,'pop2':metric2}
        ).add_to(incidents_aov)
    ind_map.add_child(incidents_aov)




    # orders count
    # users
    incidents_orders = plugins.MarkerCluster(name='Orders Made',icon_create_function=icon_create_function_gmv,
                                                           overlay=False).add_to(ind_map)
    for lat, lng, label,metric in zip(agg_data.latitude, agg_data.longitude,
                                                agg_data.city,agg_data.order_id.astype(int)):
                        MarkerWithProps(
                            location=[lat, lng],
                            icon=folium.DivIcon(html=f"""
                <div> <svg>
                <circle cx="17" cy="17" r="17" fill="#9FCC4C" opacity=".5"/>
                <circle cx="17" cy="17" r="13" fill="#9FCC4C" opacity=".5"/>
                <text x="5.5%" y="15%" text-anchor="middle">{str(metric)}</text>
                </svg></div>"""),
                            popup=label,
                            props={ 'population': metric},
                        ).add_to(incidents_orders)
    ind_map.add_child(incidents_orders)

    # product count
    # users
    incidents_products = plugins.MarkerCluster(name='Products Sold',icon_create_function=icon_create_function_gmv,
                                                           overlay=False).add_to(ind_map)
    for lat, lng, label,metric in zip(agg_data.latitude, agg_data.longitude,
                                                agg_data.city,agg_data.product_id.astype(int)):
                        MarkerWithProps(
                            location=[lat, lng],
                            icon=folium.DivIcon(html=f"""
                <div> <svg>
                <circle cx="17" cy="17" r="17" fill="#9FCC4C" opacity=".5"/>
                <circle cx="17" cy="17" r="13" fill="#9FCC4C" opacity=".5"/>
                <text x="5.5%" y="15%" text-anchor="middle">{str(metric)}</text>
                </svg></div>"""),
                            popup=label,
                            props={ 'population': metric},
                        ).add_to(incidents_products)
    ind_map.add_child(incidents_products)
    
    
    folium.LayerControl(collapsed=False).add_to(ind_map)
    map_str=ind_map._repr_html_()
    return map_str
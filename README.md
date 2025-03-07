# WeatherApp_VKyl
<p>Made using the <a href="https://www.weatherapi.com">Weather API</a></p>
<p>I've used API's 3 end-points, to implement weather casting feature</p>
<ul>
  <li>current.json (current date's weather forecast)</li>
  <li>forecats.json (1-14 day from today weather forecast)</li>
  <li>future.json (14-100 days from today weather forecast)</li>
</ul>
<code>def resolve_weather(rsa_key:str, location=None, date=None)</code>
<p>Resolves weather based on date that was entered (because of the API's specification). </p>
<p>There're 4 possible ways to resolve, 
  <code>def get_current_weather(rsa_key: str, location=None)</code>
  <code>def get_nearest_weather(rsa_key: str, location=None, days=None)</code>
  <code>def get_future_weather(rsa_key: str, location=None, date=None)</code>
All of them are used just to build a specific request URL</p>
<p>After getting weather data, before returning a response, it's passed to chatGPT with API call, to get cloth advice</p>
<h3>200 status code response structure:</h3>

> [!NOTE]
> { <br>
>  "requester_name": requester_name, <br>
>  "timestamp": end_dt.strftime("%m/%d/%Y, %H:%M:%S"), <br>
>  "location": location, <br>
>  "date": date, <br>
>  "weather": WeatherType, <br>
>  "cloth_advice": advice <br>
> }

>  [!IMPORTANT]
> WeatherType structure: <br/>
> { <br/>
> "temp_c": temerature, <br/>
> "wind_kph": wind_kph, <br/>
> "pressure_mb": pressure, <br/>
> "humidity": humidity, <br/> 
> "cast_location": location, <br/>
> "icon": icon <br/> 
> }

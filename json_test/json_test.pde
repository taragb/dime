JSONObject json;

void setup() {
  
  rect(10,10,10,10);

  json = loadJSONObject("json_schema.json");

  JSONArray values = json.getJSONArray("items");

  for (int i = 0; i < values.size(); i++) {
    
    JSONObject animal = values.getJSONObject(i); 

    String species = animal.getString("label");

    println(species);
  }
}

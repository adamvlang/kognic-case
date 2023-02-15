import json
# Setting upp base schema for open label
class BaseOpenLabelObject():
  id: str # Object id
  name: str # Object name (could be same as id)
  type: str # Object type, vehicle, animal etc.
  frame_index: str # Frame 0, 1, 2 ...
  object_geometry_format: str # format of object data, ex. bbox
  object_geometry_val: list # [x center, y center, width, height]
  object_data_name: str # name of object ex. bbox-00000001
  object_data_stream: str # Stream ex. CAM
  object_boolean_name: str # Name of object parameter of type boolean
  object_boolean_val: bool # Value of object parameter of type boolean
  object_text_name: str # Name of object paremeter of type text
  object_text_val: str # Value of object parameter of type text

  def object_definition(self):
    return {
      self.id: {
        "name": self.name,
        "type": self.type
      }
    }

  def object_data(self):
    object_geometry = {
      self.id: {
        "object_data": {
          self.object_geometry_format: [
            {
              "name": self.object_data_name,
              "stream": self.object_data_stream,
              "val": self.object_geometry_val
            }
          ]
        }
      }
    }

    try:
      boolean = {
        "boolean": [
          {
            "name": self.object_boolean_name,
            "val": self.object_boolean_val
          }
        ]
      }
      object_geometry[self.id]['object_data'] = object_geometry[self.id]['object_data'] | boolean
    except:
      pass

    try:
      text = {
        "text": [
          {
            "name": self.object_text_name,
            "val": self.object_text_val
          }
        ]
      }
      object_geometry[self.id]['object_data'] = object_geometry[self.id]['object_data'] | text
    except:
      pass
    
    return object_geometry

def convert(kognic_json):
  open_label_object_list = []

  for id in list(kognic_json['shapeProperties']):
    obj = BaseOpenLabelObject()

    obj.id = id
    obj.name = id
    obj.type = kognic_json['shapeProperties'][id]['@all']['class']
    obj.frame_index = 0 # Hardcoded since no corresponding parameter found in kognic format
    
    # Using try/except since these parameters do not always exist
    try:
      obj.object_boolean_name = "Unclear"
      obj.object_boolean_val = kognic_json['shapeProperties'][id]['@all']['Unclear']
    except:
      pass

    try:
      obj.object_text_name = "ObjectType"
      obj.object_text_val = kognic_json['shapeProperties'][id]['@all']['ObjectType']
    except:
      pass

    for sensor in list(kognic_json['shapes']):
      for feature in kognic_json['shapes'][sensor]['features']:
        if id == feature['id']:
          obj.object_data_stream = sensor    

          if feature['geometry']['type'] == "ExtremePointBox":
            obj.object_geometry_format = "bbox"
            obj.object_geometry_val = [
              feature['geometry']['coordinates']['minX']['coordinates'][0] + (feature['geometry']['coordinates']['maxX']['coordinates'][0] - feature['geometry']['coordinates']['minX']['coordinates'][0])/2,
              feature['geometry']['coordinates']['minY']['coordinates'][1] + (feature['geometry']['coordinates']['maxY']['coordinates'][1] - feature['geometry']['coordinates']['minY']['coordinates'][1])/2,
              feature['geometry']['coordinates']['maxX']['coordinates'][0] - feature['geometry']['coordinates']['minX']['coordinates'][0],
              feature['geometry']['coordinates']['maxY']['coordinates'][1] - feature['geometry']['coordinates']['minY']['coordinates'][1]
            ]
          else:
            raise NameError("Unknown gemoetry format")

          obj.object_data_name = obj.object_geometry_format + "-" + id[:8]
    open_label_object_list.append(obj)
  
  open_label_format = {
    "data": {
      "openlabel": {
        "objects": {},
        "frames": {
          "0": {
            "objects": {}  
          }
        }
      }
    }
  }

  for ol_object in open_label_object_list:
    open_label_format["data"]["openlabel"]["objects"] = open_label_format["data"]["openlabel"]["objects"] | ol_object.object_definition()
    open_label_format["data"]["openlabel"]["frames"]["0"]["objects"] = open_label_format["data"]["openlabel"]["frames"]["0"]["objects"] | ol_object.object_data()

  return json.dumps(open_label_format)

class Order < ApplicationRecord
  enum wheel: {
    "Wheel": 0,
    "Track": 1,
    "BoatPart": 2
      }
  enum engine: {
    "V8": 0,
    "Truckv12": 1,
    "L8": 2
  }
  enum gun:{
    "80mm": 0,
    "90mm": 1,
    "2x60mm": 2
  }
  enum welding:{
    Welding: 0,
    Rivets: 1,
    Bolts: 2
  }
  enum ammo: {
    ArmorPerice: 0,
    Trace: 1,
    Exploding: 2
  }
end

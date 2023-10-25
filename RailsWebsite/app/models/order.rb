class Order < ApplicationRecord
  enum type_of_tank: {red:1, blue:2,green:3}
end

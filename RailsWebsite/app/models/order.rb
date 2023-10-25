class Order < ApplicationRecord
  enum type_of_tank: {red: 0, blue: 1,green: 2}
end

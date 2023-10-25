class CreateOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :orders do |t|
      t.string :buyer
      t.string :type_of_tank
      t.boolean :completed

      t.timestamps
    end
  end
end

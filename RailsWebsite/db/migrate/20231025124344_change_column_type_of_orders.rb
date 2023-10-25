class ChangeColumnTypeOfOrders < ActiveRecord::Migration[7.1]
  def change
    change_column :orders, :type_of_tank, :integer
  end
end

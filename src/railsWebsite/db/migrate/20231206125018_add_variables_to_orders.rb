class AddVariablesToOrders < ActiveRecord::Migration[7.1]
  def change
    add_column :orders, :wheel, :string
    add_column :orders, :engine, :string
    add_column :orders, :gun, :string
    add_column :orders, :welding, :string
    add_column :orders, :ammo, :string
    add_column :orders, :isDone, :boolean
    add_column :orders, :orderDeliveredToScheduler, :boolean
  end
end

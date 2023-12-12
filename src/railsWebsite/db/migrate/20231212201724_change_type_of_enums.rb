class ChangeTypeOfEnums < ActiveRecord::Migration[7.1]
  def change
    change_column :orders, :engine, :integer
    change_column :orders, :welding, :integer
    change_column :orders, :wheel, :integer
    change_column :orders, :ammo, :integer
    change_column :orders, :gun, :integer

  end
end

class FixColumnName2 < ActiveRecord::Migration[7.1]
  def change
    rename_column :orders, :orderDeliveredToScheduler, :orderdeliveredtoscheduler

  end
end

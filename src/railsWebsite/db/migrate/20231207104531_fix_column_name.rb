class FixColumnName < ActiveRecord::Migration[7.1]
  def change
    rename_column :orders, :isDone, :isdone
  end
end

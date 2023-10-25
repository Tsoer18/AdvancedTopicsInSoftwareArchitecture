class OverviewController < ApplicationController
  def index
    @orders = Order.all
  end
end

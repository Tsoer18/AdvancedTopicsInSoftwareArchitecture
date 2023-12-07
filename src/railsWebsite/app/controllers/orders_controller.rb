class OrdersController < ApplicationController
  def new
    @order = Order.new
  end
  def create

    @order = Order.new(order_params)
    @order.isdone = false
    @order.orderdeliveredtoscheduler = false
    if @order.save
      redirect_to root_path, notice: "Lavede odre succesfuldt"
    else
      render new, status: :unprocessable_entity
    end
  end

  def index
    @orders = Order.all
  end

  def show

  end


  private

  def order_params
    params.require(:order).permit(:name, :engine, :gun, :wheel, :welding, :ammo)

  end

end

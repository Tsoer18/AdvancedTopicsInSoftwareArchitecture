class OrdersController < ApplicationController


  def index
    @orders = Order.all
  end
  def new
    @order = Order.new
    @types_of_tank = Order.type_of_tanks
  end

  def create
    @order = Order.new

    @order.assign_attributes(order_params)
    @order.completed = false
    if @order.save
      redirect_to root_path
    else
      render :new, status: :unprocessable_entity
    end
  end







  private

  def order_params
    params.require(:order).permit(:buyer,:type_of_tank)
  end
end

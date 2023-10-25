class OrdersController < ApplicationController


  def index
  end
  def new
    @order = Order.new
  end

  def create
    @order = Order.new

    @order.assign_attributes(order_params)
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

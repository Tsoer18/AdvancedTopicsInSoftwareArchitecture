class OrdersController < ApplicationController
  before_action :set_client, only: [:start]



  def index
    @orders = Order.all
  end
  def new
    @order = Order.new
    @types_of_tank = Order.type_of_tanks
  end

  def show
    @order = Order.find(params[:id])
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

  def start
    @order = Order.find(params[:id])
    puts "Hello" + @order.buyer

    @client.publish("/test", "Hello there!")
  end







  private

  def order_params
    params.require(:order).permit(:buyer,:type_of_tank)
  end

  def set_client
    @client = MqttRails::Client.new({username: 'user1', password: '1234'})
    @client.connect("localhost",1883)
  end

end

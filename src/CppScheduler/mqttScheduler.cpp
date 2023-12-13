#include <iostream>
#include <cstdlib>
#include <string>
#include <cstring>
#include <cctype>
#include <thread>
#include <chrono>
#include <vector>
#include <nlohmann/json.hpp>
#include <mqtt/async_client.h>

using json = nlohmann::json;

// Client viarbales
const std::string ADDRESS = "tcp://mqtt5monitor:1884";
const std::string CLIENT_ID("cpp_publisher_subscriber");
const std::string USERNAME{"user1"};
const std::string PASSWORD{"1234"};
const int QOS = 2;
const int N_RETRY_ATTEMPTS = 5;

// Subcribe Topics
const std::string TOPICR("Sensors/WheelR/Robots");
const std::string TOPICERROR("Robots/Error/NoHeartBeat");
const std::string TOPICORDER("Scheduler/order/newOrder");

// Publish Topics
const std::string TOPICCONFIGURATIONSYSTEM("Config/Robots");
const std::string TOPICINVENTORYSYSTEM("Check/Inventory");
const std::string TOPICSCHEDULE("Schedule/");
const std::string TOPICROBOTORDER("Robots/Order");
const std::string TOPICM("Hello");
const std::string TOPICERRORTEST("Robots/Error/NoHeartBeat/Test");
const std::string TOPICWEBSITE("Website/");
const std::string TOPICRECIEVEDORDER("Scheduler/order/recievedOrder");
const std::string TOPICORDERDONE("Scheduler/order/done");

// Order list
std::vector<json> orderList;
std::vector<json> CheckList;
int Currentorder;

class action_listener : public virtual mqtt::iaction_listener
{
    std::string name_;

    void on_failure(const mqtt::token &tok) override
    {
        std::cout << name_ << " failure";
        if (tok.get_message_id() != 0)
            std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
        std::cout << std::endl;
    }

    void on_success(const mqtt::token &tok) override
    {
        std::cout << name_ << " success";
        if (tok.get_message_id() != 0)
            std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
        auto top = tok.get_topics();
        if (top && !top->empty())
            std::cout << "\ttoken topic: '" << (*top)[0] << "', ..." << std::endl;
        std::cout << std::endl;
    }

public:
    action_listener(const std::string &name) : name_(name) {}
};

/////////////////////////////////////////////////////////////////////////////

class callback : public virtual mqtt::callback,
                 public virtual mqtt::iaction_listener

{
    // Counter for the number of connection retries
    int nretry_;
    // The MQTT client
    mqtt::async_client &cli_;
    // Options to use if we need to reconnect
    mqtt::connect_options &connOpts_;
    // An action listener to display the result of actions.
    action_listener subListener_;

    // This deomonstrates manually reconnecting to the broker by calling
    // connect() again. This is a possibility for an application that keeps
    // a copy of it's original connect_options, or if the app wants to
    // reconnect with different options.
    // Another way this can be done manually, if using the same options, is
    // to just call the async_client::reconnect() method.
    void reconnect()
    {
        std::this_thread::sleep_for(std::chrono::milliseconds(2500));
        try
        {
            cli_.connect(connOpts_, nullptr, *this);
        }
        catch (const mqtt::exception &exc)
        {
            std::cerr << "Error: " << exc.what() << std::endl;
            exit(1);
        }
    }

    // Re-connection failure
    void on_failure(const mqtt::token &tok) override
    {
        std::cout << "Connection attempt failed" << std::endl;
        if (++nretry_ > N_RETRY_ATTEMPTS)
            exit(1);
        reconnect();
    }

    // (Re)connection success
    // Either this or connected() can be used for callbacks.
    void on_success(const mqtt::token &tok) override {}

    // (Re)connection success
    void connected(const std::string &cause) override
    {
        std::cout << "\nConnection success" << std::endl;
        std::cout << "\nSubscribing to topic '" << TOPICR << "'\n"
                  << "\tfor client " << CLIENT_ID
                  << " using QoS" << QOS << "\n"
                  << std::endl;

        cli_.subscribe(TOPICR, QOS, nullptr, subListener_);
        cli_.subscribe(TOPICERROR, QOS, nullptr, subListener_);
        cli_.subscribe(TOPICORDER, QOS, nullptr, subListener_);
    }

    // Callback for when the connection is lost.
    // This will initiate the attempt to manually reconnect.
    void connection_lost(const std::string &cause) override
    {
        std::cout << "\nConnection lost" << std::endl;
        if (!cause.empty())
            std::cout << "\tcause: " << cause << std::endl;

        std::cout << "Reconnecting..." << std::endl;
        nretry_ = 0;
        reconnect();
    }

    void CheckInventory(json order)
    {

        std::string payload = order.dump();

        auto msg = mqtt::make_message(TOPICINVENTORYSYSTEM, payload);
        msg->set_qos(QOS);
        cli_.publish(msg);
        std::cout << "check inventory msg sent" << std::endl;
    }

    json configuredOrder(json order)
    {
        std::string payload = order.dump();
        auto msg = mqtt::make_message(TOPICCONFIGURATIONSYSTEM, payload);
        msg->set_qos(QOS);
        cli_.publish(msg);
        std::cout << "Config msg sent " << std::endl;

        int wheel = order["Wheel"];
        std::string wheelFunction;
        if (wheel == 0)
        {
            wheelFunction = "180z,120x,90y";
        }
        else if (wheel == 1)
        {
            wheelFunction = "120z,20x,70y";
        }
        else if (wheel == 2)
        {
            wheelFunction = "30z,10x,30y";
        }
        else
        {
            wheelFunction = "30z,10x,30y";
        }
        int engine = order["Engine"];
        std::string engineFunction;
        if (engine == 0)
        {
            engineFunction = "180z,120x,90y";
        }
        else if (engine == 1)
        {
            engineFunction = "120z,20x,70y";
        }
        else if (engine == 2)
        {
            engineFunction = "30z,10x,30y";
        }
        else
        {
            engineFunction = "30z,10x,30y";
        }
        int gun = order["Gun"];
        std::string gunFunction;
        if (gun == 0)
        {
            gunFunction = "180z,120x,90y";
        }
        else if (gun == 1)
        {
            gunFunction = "120z,20x,70y";
        }
        else if (gun == 2)
        {
            gunFunction = "30z,10x,30y";
        }
        else
        {
            gunFunction = "30z,10x,30y";
        }
        int welding = order["Welding"];
        std::string weldingFunction;
        if (welding == 0)
        {
            weldingFunction = "180z,120x,90y";
        }
        else if (welding == 1)
        {
            weldingFunction = "120z,20x,70y";
        }
        else if (welding == 2)
        {
            weldingFunction = "30z,10x,30y";
        }
        else
        {
            weldingFunction = "30z,10x,30y";
        }
        int ammo = order["Ammo"];
        std::string ammoFunction;
        if (ammo == 0)
        {
            ammoFunction = "180z,120x,90y";
        }
        else if (ammo == 1)
        {
            ammoFunction = "120z,20x,70y";
        }
        else if (ammo == 2)
        {
            ammoFunction = "30z,10x,30y";
        }
        else
        {
            ammoFunction = "30z,10x,30y";
        }
        int orderID = order["orderID"];

        json orderDetail;
        orderDetail["orderID"] = orderID;
        orderDetail["wheelfunction"] = wheelFunction;
        orderDetail["enginefunction"] = engineFunction;
        orderDetail["gunfunction"] = gunFunction;
        orderDetail["weldingfunction"] = weldingFunction;
        orderDetail["ammofunction"] = ammoFunction;

        return orderDetail;
    }

    void orderHandling(mqtt::const_message_ptr msg)
    {
        std::string payload = msg->to_string();
        std::cout << "Order message received: " << payload << std::endl;

        try
        {
            // Parse JSON payload
            json orderJson = json::parse(payload);
            int orderID = orderJson["orderID"];
            json jspayload;
            jspayload["Message"] = "Order " + std::to_string(orderID) + " has been received";
            jspayload["orderid"] = orderID;
            std::string payloadw = jspayload.dump();

            std::cout << payloadw << std::endl;
            auto msgw = mqtt::make_message(TOPICRECIEVEDORDER, payloadw);
            msgw->set_qos(QOS);
            cli_.publish(msgw);
            // CheckInventorySystem
            CheckInventory(orderJson);

            // Convert Order to Robot Function
            json orderConfiguration = configuredOrder(orderJson);

            // inputRobot Function order to schedule
            orderList.push_back(orderConfiguration);
            std::cout << "Schedule msg sent " << std::endl;
        }
        catch (const std::exception &e)
        {
            std::cerr << "Error parsing order JSON: " << e.what() << std::endl;
            // Handle the error as needed
        }
    }

    void errorHandling(mqtt::const_message_ptr msg)

    {
        std::string payload = msg->to_string();
        std::cout << "Error message received:" << payload << std::endl;
        if (payload == "No Dough")
        {
            std::string payload1 = "Shut Down Robot and replace/fix";
            std::cout << "Error Message sent" << std::endl;
            auto msg1 = mqtt::make_message(TOPICERRORTEST, payload1);
            msg1->set_qos(QOS);
            cli_.publish(msg1);

            auto msgw = mqtt::make_message(TOPICWEBSITE, payload1);
            msgw->set_qos(QOS);
            cli_.publish(msgw);
        }
    }

    void robotHandling(mqtt::const_message_ptr msg)
    {
        std::string payload = msg->to_string();
        std::cout << "Robot message received: " << payload << std::endl;
        try
        {
            // Parse JSON payload
            json RobotSensor = json::parse(payload);

            std::string status = RobotSensor["status"];
            if (status == "Done")
            {
                if (!orderList.empty())
                {

                    if (Currentorder != 0)
                    {
                        json jspayload;
                        jspayload["Message"] = "Order " + std::to_string(Currentorder) + " is Finsihed";
                        jspayload["orderid"] = Currentorder;
                        std::string payloads = jspayload.dump();
                        std::cout << payloads << std::endl;
                        auto msg = mqtt::make_message(TOPICORDERDONE, payloads);
                        msg->set_qos(QOS);
                        cli_.publish(msg);
                    }
                    else
                    {
                        json jspayload;
                        jspayload["Message"] = "Start up done";
                        jspayload["orderid"] = 0000;
                        std::string payloads = jspayload.dump();
                        std::cout << payloads << std::endl;
                        auto msg = mqtt::make_message(TOPICORDERDONE, payloads);
                        msg->set_qos(QOS);
                        cli_.publish(msg);
                    }
                    json robotF = orderList.front();
                    orderList.erase(orderList.begin());
                    Currentorder = robotF["orderID"];
                    std::string fpayload = robotF.dump();
                    auto msg = mqtt::make_message(TOPICROBOTORDER, fpayload);
                    msg->set_qos(QOS);
                    cli_.publish(msg);
                    std::cout << "robot order sent" << std::endl;
                }
                else
                {
                    if (Currentorder != 0)
                    {
                        json jspayload;
                        jspayload["Message"] = "Order " + std::to_string(Currentorder) + " is Finsihed and orderlist is empty";
                        jspayload["orderid"] = Currentorder;
                        std::string payloads = jspayload.dump();
                        std::cout << payloads << std::endl;
                        auto msg = mqtt::make_message(TOPICORDERDONE, payloads);
                        msg->set_qos(QOS);
                        cli_.publish(msg);
                        Currentorder = 0;
                    }
                    else
                    {
                        json jspayload;
                        jspayload["Message"] = "Start up done/or no current order and orderlist is empty";
                        jspayload["orderid"] = 0000;
                        std::string payloads = jspayload.dump();
                        std::cout << payloads << std::endl;
                        auto msg = mqtt::make_message(TOPICORDERDONE, payloads);
                        msg->set_qos(QOS);
                        cli_.publish(msg);
                    }
                    std::cout << "orderList is empty" << std::endl;
                }
            }
        }
        catch (const std::exception &e)
        {
            std::cerr << "Error parsing order JSON: " << e.what() << std::endl;
            // Handle the error as needed
        }
    }
    // Callback for when a message arrives.
    void message_arrived(mqtt::const_message_ptr msg) override
    {
        std::string currentTopic = msg->get_topic();
        std::cout << "Message arrived" << std::endl;
        std::cout << "\ttopic: " << currentTopic << std::endl;
        if (currentTopic == TOPICORDER)
        {
            std::cout << "Order Handling" << std::endl;
            orderHandling(msg);
        }
        else if (currentTopic == TOPICERROR)
        {
            std::cout << "Error Handling" << std::endl;
            errorHandling(msg);
        }
        else if (currentTopic == TOPICR)
        {
            std::cout << "Robot Handling" << std::endl;
            robotHandling(msg);
        }
    }

    void delivery_complete(mqtt::delivery_token_ptr token) override {}

public:
    callback(mqtt::async_client &cli, mqtt::connect_options &connOpts)
        : nretry_(0), cli_(cli), connOpts_(connOpts), subListener_("Subscription") {}
};

int main()
{
    mqtt::async_client cli(ADDRESS, CLIENT_ID, mqtt::create_options(MQTTVERSION_5));

    auto connOpts = mqtt::connect_options_builder()
                        .user_name(USERNAME)
                        .password(PASSWORD)
                        .mqtt_version(MQTTVERSION_5)
                        .clean_start(true) // v5 specific
                        .finalize();

    callback cb(cli, connOpts);
    cli.set_callback(cb);

    try
    {
        cli.connect(connOpts)->wait();
        std::cout << "Connected to the MQTT broker" << std::endl;

        // Publish a message
        std::string payload = "Hello, MQTT!";
        auto msg = mqtt::make_message(TOPICM, payload);
        msg->set_qos(QOS);
        cli.publish(msg)->wait();
        std::cout << "Message published: " << payload << std::endl;

        // Keep the program running to receive messages
        while (true)
        {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
    catch (const mqtt::exception &exc)
    {
        std::cerr << "Error: " << exc.what() << std::endl;
        return 1;
    }

    return 0;
}
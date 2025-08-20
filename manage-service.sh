#!/bin/bash

# Medical Referral App Service Management Script

case "$1" in
    start)
        echo "Starting Medical Referral App service..."
        sudo systemctl start referral-app.service
        echo "Service started!"
        ;;
    stop)
        echo "Stopping Medical Referral App service..."
        sudo systemctl stop referral-app.service
        echo "Service stopped!"
        ;;
    restart)
        echo "Restarting Medical Referral App service..."
        sudo systemctl restart referral-app.service
        echo "Service restarted!"
        ;;
    status)
        echo "Medical Referral App service status:"
        sudo systemctl status referral-app.service
        ;;
    logs)
        echo "Medical Referral App service logs:"
        sudo journalctl -u referral-app.service -f
        ;;
    enable)
        echo "Enabling Medical Referral App service to start on boot..."
        sudo systemctl enable referral-app.service
        echo "Service enabled!"
        ;;
    disable)
        echo "Disabling Medical Referral App service from starting on boot..."
        sudo systemctl disable referral-app.service
        echo "Service disabled!"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|enable|disable}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the service"
        echo "  stop     - Stop the service"
        echo "  restart  - Restart the service"
        echo "  status   - Show service status"
        echo "  logs     - Show service logs (real-time)"
        echo "  enable   - Enable service to start on boot"
        echo "  disable  - Disable service from starting on boot"
        echo ""
        echo "App URL: http://192.168.50.57:5000/"
        exit 1
        ;;
esac

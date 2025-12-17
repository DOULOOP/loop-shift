#!/bin/bash
# Quick start script for the continuous card listener

echo "=========================================="
echo "  Starting Card Listener Service"
echo "=========================================="
echo ""

# Check if containers are running
if ! docker ps | grep -q loop_shift_app; then
    echo "Starting all services..."
    docker-compose up -d
else
    echo "Services already running."
fi

echo ""
echo "Card listener is now active!"
echo ""
echo "Commands:"
echo "  View logs:  docker logs -f loop_shift_listener"
echo "  Stop:       docker-compose stop card_listener"
echo "  Restart:    docker-compose restart card_listener"
echo ""
echo "Press Ctrl+C to exit this script (listener will continue running)"
echo "=========================================="
echo ""

# Follow logs
docker logs -f loop_shift_listener


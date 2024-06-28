document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    const eventTypes = ['click', 'page_view'];

    function fetchEventData(eventType) {
        console.log(`Fetching ${eventType} data`);
        fetch(`/get_event_data?event_type=${eventType}`)
            .then(response => response.json())
            .then(data => {
                console.log(`Fetched ${eventType} data:`, data);
                updateTable(eventType, data);
            })
            .catch(error => console.error(`Error fetching ${eventType} data:`, error));
    }

    function createTableContainer(eventType) {
        const tableId = `${eventType === 'page_view' ? 'pageView' : eventType}Table`;
        console.log(`Looking for table element with id ${tableId}`);
        const tableElement = document.getElementById(tableId);
        if (!tableElement) {
            console.error(`Cannot find table element with id ${tableId}`);
            return null;
        }
        console.log(`Found table element with id ${tableId}`);
        return tableElement;
    }

    const tables = {};
    eventTypes.forEach(eventType => {
        console.log(`Creating table container for event type ${eventType}`);
        const table = createTableContainer(eventType);
        if (table) {
            tables[eventType] = table;
            fetchEventData(eventType);
            setInterval(() => fetchEventData(eventType), 5000); // Fetch data every 5 seconds
        }
    });

    function updateTable(eventType, data) {
        const table = tables[eventType];
        if (table) {
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = ''; // Clear previous rows

            data.forEach(row => {
                const tr = document.createElement('tr');
                const tdDate = document.createElement('td');
                tdDate.textContent = row.timestamp;
                const tdCount = document.createElement('td');
                tdCount.textContent = row.count;
                tr.appendChild(tdDate);
                tr.appendChild(tdCount);
                tbody.appendChild(tr);
            });
        }
    }
});

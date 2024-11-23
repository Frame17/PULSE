# Pulse: Pragmatic Unified Layout for Structured Economics 🌍📈

Pulse is a lightweight and flexible application that aggregates economic data from multiple sources and integrates seamlessly with **Grafana** via the **Infinity Plugin**. It simplifies the process of accessing, processing, and visualizing global economic indicators, providing valuable insights into financial trends.

---

## 🚀 Features
- **Multi-Provider Support**: Fetch data from:
  - 📊 **FRED (Federal Reserve Economic Data)**
  - 🏦 **ECB (European Central Bank)**
  - 📈 **Eurostat (European Statistics)**
- **Grafana-Ready**: Direct integration with Grafana's **Infinity Plugin** for customizable dashboards.
- **Flexible Query Parameters**:
  - Filter by `series_id`, `frequency`, and custom `filter_key`.
  - Apply time offsets for historical data adjustments.
- **Simple API**: RESTful endpoints for quick and easy data retrieval.

---

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher (if running manually)
- `docker` and `docker-compose` for containerized deployment
- [Grafana Infinity Plugin](https://grafana.com/grafana/plugins/yesoreyeram-infinity-datasource/)

---

### Docker Deployment
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pulse.git
   cd pulse
   ```

2. Configure environment variables:
   - Create a `.env` file in the project root.
   - Add your **FRED API Key**:
     ```env
     FRED_API_KEY=your_fred_api_key
     ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. The application will be available at:
   ```
   http://localhost:8000/pulse
   ```

---

## 📡 API Usage

### Endpoint: `/pulse`
**Description**: Fetch economic data in a Grafana-compatible format.

#### Parameters:
| Parameter    | Type   | Default | Description                                   |
|--------------|--------|---------|-----------------------------------------------|
| `provider`   | string | `FRED`  | Data source (`FRED`, `EUROSTAT`, or `ECB`).  |
| `series_id`  | string | None    | Unique identifier for the data series.       |
| `frequency`  | string | `d`     | Data frequency (`d` for daily, `m` for monthly, `q` for quarterly, , `a` for annually). |
| `filter_key` | string | None    | Optional filter for narrowing data results.  |
| `offset`     | int    | None    | Shift timestamps by a specific number of years. |

#### Example Request:
```bash
GET http://localhost:8000/pulse?provider=fred&series_id=A191RL1Q225SBEA&frequency=q
```

#### Example Response:
```json
[
	{
		"timestamp": "2024-04-01",
		"value": 3.0
	},
	{
		"timestamp": "2024-07-01",
		"value": 2.8
	}
]
```

---

## 📊 Grafana Integration
1. Install and configure the **Infinity Plugin** in Grafana.
2. Add a new data source and set the type to **Infinity**.
3. Configure the API endpoint:
   - URL: `http://pulse:8000/pulse`
   - Method: `GET`
   - Add query parameters like `provider`, `series_id`, etc.
4. Create dashboards using the fetched data!

---

## 🧩 Extending Providers
Adding new data sources is simple:
1. Implement the `DataProvider` interface in `pulse.providers.provider`.
2. Add the new provider to the `PROVIDERS` dictionary for the request routing.

---

## 🤝 Contributing
We welcome contributions! Please:
- Fork the repository.
- Submit a pull request with detailed explanations.

---

## 🛡️ License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 👨‍💻 Author
Created with ❤️ by **[Serhii Fedusov](https://github.com/your-username)** with the support from Anastasiia Shablienko.
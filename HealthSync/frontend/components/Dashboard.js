import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [healthMetrics, setHealthMetrics] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchHealthMetrics = async () => {
            try {
                const response = await axios.get('/api/health-metrics');
                setHealthMetrics(response.data);
            } catch (err) {
                setError('Failed to fetch health metrics');
            } finally {
                setLoading(false);
            }
        };

        fetchHealthMetrics();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard">
            <h1>User Health Dashboard</h1>
            <div className="metrics">
                {healthMetrics.length > 0 ? (
                    healthMetrics.map((metric) => (
                        <div key={metric.id} className="metric">
                            <h2>{metric.name}</h2>
                            <p>Value: {metric.value}</p>
                            <p>Date: {new Date(metric.date).toLocaleDateString()}</p>
                        </div>
                    ))
                ) : (
                    <p>No health metrics available.</p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
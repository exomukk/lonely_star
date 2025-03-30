import React from 'react';
import './leaderboard.css';

function Leaderboard() {
    // Dữ liệu mẫu (có thể thay bằng props hoặc dữ liệu fetch từ API)
    const players = [
        { rank: 1, name: 'creammjnk', score: 2500 },
        { rank: 2, name: 'winter', score: 2000 },
        { rank: 3, name: 'exomuk', score: 1800 },
        { rank: 4, name: 'sonbx', score: 1600 },
        { rank: 5, name: 'vanhphan', score: 1500 },
    ];

    return (
        <div className="leaderboard-page">
            <div className="leaderboard-container">
                <h2>Top Players</h2>
                <table className="leaderboard-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Name</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {players.map((player) => {
                            // Tạo className cho top 3 để tô màu khác
                            let rankClass = '';
                            if (player.rank === 1) rankClass = 'rank-1';
                            if (player.rank === 2) rankClass = 'rank-2';
                            if (player.rank === 3) rankClass = 'rank-3';

                            return (
                                <tr key={player.rank}>
                                    <td className={rankClass}>{player.rank}</td>
                                    <td>{player.name}</td>
                                    <td>{player.score}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default Leaderboard;

#include <iostream>
#include <map>
#include <queue>
#include <vector>
#include <climits>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string start, end;
    cin >> start >> end;

    // Graph with distances
    map<string, map<string, int>> graph;
    graph["Delhi"]["Jaipur"] = 280;
    graph["Delhi"]["Agra"] = 210;
    graph["Jaipur"]["Delhi"] = 280;
    graph["Jaipur"]["Udaipur"] = 390;
    graph["Agra"]["Delhi"] = 210;
    graph["Agra"]["Kanpur"] = 270;
    graph["Udaipur"]["Jaipur"] = 390;
    graph["Udaipur"]["Ahmedabad"] = 260;
    graph["Kanpur"]["Agra"] = 270;
    graph["Kanpur"]["Lucknow"] = 90;
    graph["Ahmedabad"]["Udaipur"] = 260;
    graph["Ahmedabad"]["Mumbai"] = 530;
    graph["Lucknow"]["Kanpur"] = 90;
    graph["Lucknow"]["Varanasi"] = 320;
    graph["Lucknow"]["Mumbai"] = 1360;
    graph["Mumbai"]["Ahmedabad"] = 530;
    graph["Mumbai"]["Varanasi"] = 1420;
    graph["Mumbai"]["Lucknow"] = 1360;
    graph["Varanasi"]["Lucknow"] = 320;
    graph["Varanasi"]["Mumbai"] = 1420;

    // Distance and parent maps
    map<string, int> dist;
    map<string, string> parent;

    for (auto it : graph)
        dist[it.first] = INT_MAX;

    dist[start] = 0;

    // Min-heap for Dijkstra
    priority_queue<pair<int, string>, vector<pair<int, string>>, greater<pair<int, string>>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
        auto current = pq.top();
        pq.pop();

        int d = current.first;
        string node = current.second;

        if (d > dist[node]) continue;

        for (auto it : graph[node]) {
            string nbr = it.first;
            int w = it.second;

            if (dist[nbr] > d + w) {
                dist[nbr] = d + w;
                parent[nbr] = node;
                pq.push({dist[nbr], nbr});
            }
        }
    }

    if (dist[end] == INT_MAX) {
        cout << "NoPath";
        return 0;
    }

    vector<string> path;
    string cur = end;

    while (cur != start) {
        path.push_back(cur);
        cur = parent[cur];
    }

    path.push_back(start);
    reverse(path.begin(), path.end());

    cout << dist[end] << "\n";
    for (int i = 0; i < path.size(); i++) {
        cout << path[i];
        if (i != path.size() - 1)
            cout << " ";
    }

    return 0;
}

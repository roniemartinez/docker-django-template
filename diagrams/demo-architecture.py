from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Django

with Diagram("Architecture", filename="diagrams/demo-architecture", show=True, graph_attr={"margin": "-1.8"}):
    browser = Custom("browser", str(Path(__file__).parent / "chrome_128x128.png"))

    cluster_graph_attr = {"margin": "8"}

    with Cluster("Digital Ocean Droplet", graph_attr=cluster_graph_attr):
        system_nginx = Nginx("system_nginx")

        with Cluster("Docker", graph_attr=cluster_graph_attr):
            nginx = Nginx("nginx")
            django = Django("django")
            database = PostgreSQL("postgres")

    browser - Edge(style="dotted") >> system_nginx >> nginx >> django >> database

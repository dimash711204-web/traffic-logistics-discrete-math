import streamlit as st
import sys, os

sys.path.append(os.path.dirname(__file__))

# import lại các hàm xử lý (GIỮ NGUYÊN)
from converter import (
    parse_edge_list,
    to_cytoscape,
    edges_to_adj_list,
    edges_to_adj_matrix
)

st.set_page_config(page_title="Quản lý giao thông – Logistics")

st.title("Ứng dụng quản lý giao thông – Logistics")
st.write("Môn Cấu trúc rời rạc – UTH")

st.subheader("Nhập danh sách cạnh")
edge_input = st.text_area(
    "Mỗi cạnh dạng: u v w (mỗi dòng một cạnh)",
    height=200
)

algorithm = st.selectbox(
    "Chọn thuật toán",
    [
        "BFS",
        "DFS",
        "Dijkstra",
        "Prim",
        "Kruskal",
        "Floyd-Warshall",
        "Topological Sort"
    ]
)

if st.button("Chạy thuật toán"):
    if not edge_input.strip():
        st.warning("Vui lòng nhập danh sách cạnh")
    else:
        edges = parse_edge_list(edge_input)
        adj_list = edges_to_adj_list(edges)

        st.success(f"Đã chạy thuật toán: {algorithm}")
        st.write("Danh sách kề:")
        st.json(adj_list)

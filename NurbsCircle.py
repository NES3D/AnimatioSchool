import maya.cmds as cmds
import maya.api.OpenMaya as om

def create_pipe_along_edges(radius=0.1):  # Добавляем параметр для радиуса
    # Получаем активный выбор
    sel_list = om.MGlobal.getActiveSelectionList()
    if sel_list.length() == 0:
        print("Выберите объект на сцене.")
        return

    # Получаем путь к первому выделенному объекту
    dag_path = sel_list.getDagPath(0)
    
    # Проверка на тип объекта
    if not dag_path.hasFn(om.MFn.kMesh):
        print("Выделенный объект не является полигональной сеткой.")
        return
    
    # Создаём итератор по рёбрам
    edge_iter = om.MItMeshEdge(dag_path)
    
    while not edge_iter.isDone():
        # Получаем индексы вершин ребра
        vtx1, vtx2 = edge_iter.vertexId(0), edge_iter.vertexId(1)
        
        # Получаем мировые координаты вершин
        point1 = om.MFnMesh(dag_path).getPoint(vtx1, om.MSpace.kWorld)
        point2 = om.MFnMesh(dag_path).getPoint(vtx2, om.MSpace.kWorld)
        
        # Вычисляем нормаль ребра
        edge_vector = om.MVector(point2 - point1).normal()
        
        # Создаём NURBS-кривую
        curve_name = cmds.curve(d=1, p=[(point1.x, point1.y, point1.z), (point2.x, point2.y, point2.z)])
        
        # Создаём NURBS-круг с нормалью вдоль ребра и заданным радиусом
        circle_name = cmds.circle(nr=(edge_vector.x, edge_vector.y, edge_vector.z), c=(point1.x, point1.y, point1.z), radius=radius, ch=False)[0]
        
        # Экструзия NURBS-круга по NURBS-кривой
        pipe_name = cmds.extrude(circle_name, curve_name, ch=False, rn=False, po=0)[0]
        
        # Удаляем исходные кривую и круг
        cmds.delete(curve_name, circle_name)
        
        # Переходим к следующему ребру
        edge_iter.next()

create_pipe_along_edges(radius=0.05)

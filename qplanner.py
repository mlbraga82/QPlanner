from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsPalLayerSettings,
    QgsTextFormat,
    QgsVectorLayerSimpleLabeling,
)
from PyQt5.QtCore import QVariant, QTime
from PyQt5.QtWidgets import QInputDialog
from datetime import datetime, timedelta

# Função para validar e converter horário de partida
def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Função para calcular o horário de passagem
def calculate_passage_time(start_time, distance, speed_ms):
    if speed_ms == 0:
        return start_time
    seconds = distance / speed_ms
    start_datetime = datetime.strptime(start_time, "%H:%M")
    passage_time = start_datetime + timedelta(seconds=seconds)
    return passage_time.strftime("%H:%M:%S")

# Função principal para criar pontos ao longo de uma linha
def create_points_along_line():
    # Obter a camada ativa
    layer = iface.activeLayer()
    
    # Verificar se a camada é válida e do tipo linha
    if not layer or layer.geometryType() != 1:  # 1 = Line
        iface.messageBar().pushMessage("Erro", "Selecione uma camada de linha válida!", level=3)
        return
    
    # Solicitar a distância de intervalo ao usuário
    distance_interval, ok = QInputDialog.getDouble(
        iface.mainWindow(), 
        "Distância de Intervalo", 
        "Digite a distância de intervalo (em metros):", 
        10.0, 0.0, 1000000.0, 2
    )
    
    if not ok:
        iface.messageBar().pushMessage("Cancelado", "Operação cancelada pelo usuário.", level=1)
        return
    
    # Solicitar o horário de partida
    start_time, ok = QInputDialog.getText(
        iface.mainWindow(),
        "Horário de Partida",
        "Digite o horário de partida (formato HH:MM):",
        text="08:00"
    )
    
    if not ok:
        iface.messageBar().pushMessage("Cancelado", "Operação cancelada pelo usuário.", level=1)
        return
    
    if not validate_time(start_time):
        iface.messageBar().pushMessage("Erro", "Horário inválido! Use o formato HH:MM.", level=3)
        return
    
    # Solicitar a velocidade média
    speed_kmh, ok = QInputDialog.getDouble(
        iface.mainWindow(),
        "Velocidade Média",
        "Digite a velocidade média (em km/h):",
        60.0, 0.0, 1000.0, 2
    )
    
    if not ok:
        iface.messageBar().pushMessage("Cancelado", "Operação cancelada pelo usuário.", level=1)
        return
    
    # Converter velocidade de km/h para m/s
    speed_ms = speed_kmh * 1000 / 3600
    
    # Criar transformação para EPSG:3857
    source_crs = layer.crs()
    dest_crs = QgsCoordinateReferenceSystem("EPSG:3857")
    transform_to_3857 = QgsCoordinateTransform(source_crs, dest_crs, QgsProject.instance())
    transform_to_original = QgsCoordinateTransform(dest_crs, source_crs, QgsProject.instance())
    
    # Criar uma nova camada de pontos no CRS original
    crs = layer.crs().authid()
    point_layer = QgsVectorLayer(f"Point?crs={crs}", "Pontos_ao_Longo_da_Linha", "memory")
    provider = point_layer.dataProvider()
    
    # Adicionar campos para distância e horário
    provider.addAttributes([
        QgsField("Distancia", QVariant.Double),
        QgsField("Horario", QVariant.String)
    ])
    point_layer.updateFields()
    
    # Configurar rótulos no formato HH:MM
    label_settings = QgsPalLayerSettings()
    label_settings.fieldName = "left(Horario, 5)"  # Extrai HH:MM de HH:MM:SS
    label_settings.enabled = True
    text_format = QgsTextFormat()
    label_settings.setFormat(text_format)
    labeling = QgsVectorLayerSimpleLabeling(label_settings)
    point_layer.setLabeling(labeling)
    point_layer.setLabelsEnabled(True)
    
    # Iniciar edição na nova camada
    point_layer.startEditing()
    
    # Iterar sobre as feições da camada de linha
    for feature in layer.getFeatures():
        geom = feature.geometry()
        # Transformar geometria para EPSG:3857
        geom_3857 = QgsGeometry(geom)
        geom_3857.transform(transform_to_3857)
        
        if geom_3857.isMultipart():
            lines = geom_3857.asMultiPolyline()
        else:
            lines = [geom_3857.asPolyline()]
        
        for line in lines:
            length = geom_3857.length()
            current_distance = 0.0
            
            # Criar pontos ao longo da linha com intervalo fixo
            while current_distance <= length:
                point_3857 = geom_3857.interpolate(current_distance)
                if point_3857:
                    # Transformar o ponto de volta para o CRS original
                    point_original = QgsGeometry(point_3857)
                    point_original.transform(transform_to_original)
                    feat = QgsFeature()
                    feat.setGeometry(point_original)
                    # Calcular horário de passagem
                    passage_time = calculate_passage_time(start_time, current_distance, speed_ms)
                    feat.setAttributes([current_distance, passage_time])
                    provider.addFeature(feat)
                current_distance += distance_interval
            
            # Forçar a criação do último ponto, se necessário
            if current_distance - distance_interval < length:
                point_3857 = geom_3857.interpolate(length)
                if point_3857:
                    point_original = QgsGeometry(point_3857)
                    point_original.transform(transform_to_original)
                    feat = QgsFeature()
                    feat.setGeometry(point_original)
                    passage_time = calculate_passage_time(start_time, length, speed_ms)
                    feat.setAttributes([length, passage_time])
                    provider.addFeature(feat)
    
    # Finalizar edição e salvar
    point_layer.commitChanges()
    
    # Adicionar a camada ao projeto
    QgsProject.instance().addMapLayer(point_layer)
    iface.messageBar().pushMessage("Sucesso", "Pontos criados com sucesso!", level=0)

# Executar a função
create_points_along_line()

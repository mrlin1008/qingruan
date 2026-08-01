/**
 * 益阳高新区智慧招商平台 — 地图通用模块
 * 依赖 Leaflet.js
 */
(function () {
  'use strict';

  // 赛道颜色映射
  var TRACK_COLORS = {
    '智能感知': '#3b82f6',
    '工业视觉': '#0ca678',
    '装备智能': '#f08c00',
    '算力配套': '#8b5cf6'
  };

  /**
   * 初始化地图
   * @param {string} containerId - 地图容器 div id
   * @param {object} options - {center: [lat, lng], zoom: number}
   */
  window.initInvestmentMap = function (containerId, options) {
    options = options || {};
    var map = L.map(containerId, {
      center: options.center || [28.55, 112.35],
      zoom: options.zoom || 10
    });

    // 高德地图瓦片
    L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
      subdomains: '1234',
      maxZoom: 18,
      attribution: '高德地图 &copy; AutoNavi'
    }).addTo(map);

    return map;
  };

  /**
   * 在地图上标注企业
   * @param {L.Map} map - Leaflet 地图实例
   * @param {Array} companies - [{name, lat, lng, track, type, city}]
   */
  window.markCompanies = function (map, companies) {
    var markers = [];
    companies.forEach(function (c) {
      if (!c.lat || !c.lng) return;
      var color = TRACK_COLORS[c.track] || '#1e5bff';
      var radius = c.type === 'settled' ? 8 : 6;

      var marker = L.circleMarker([c.lat, c.lng], {
        radius: radius,
        fillColor: color,
        color: '#fff',
        weight: 2,
        fillOpacity: 0.85
      })
      .bindPopup(
        '<b>' + c.name + '</b><br>' +
        (c.track || '未分类') + ' · ' + (c.city || '') +
        '<br><small>' + (c.type === 'settled' ? '入驻企业' : '目标客商') + '</small>'
      )
      .addTo(map);

      markers.push(marker);
    });
    return markers;
  };

  /**
   * 在地图上叠加产业密度热力图
   * @param {L.Map} map - Leaflet 地图实例
   * @param {Array} points - [{lat, lng, intensity}, ...]
   * @param {object} options - 可选配置
   */
  window.addHeatmapLayer = function (map, points, options) {
    options = options || {};
    if (!points || points.length === 0) return null;

    var heatPoints = points.map(function (p) {
      return [p.lat, p.lng, p.intensity || 0.3];
    });

    var layer = L.heatLayer(heatPoints, {
      radius: options.radius || 35,
      blur: options.blur || 25,
      maxZoom: options.maxZoom || 14,
      max: options.max || 1.0,
      gradient: options.gradient || {
        0.1: '#2ecc71',
        0.3: '#66cc00',
        0.5: '#ffcc00',
        0.7: '#ff9900',
        0.9: '#ff3300'
      }
    }).addTo(map);

    return layer;
  };

})();

<template>
	<el-tabs type="border-card" v-model="activeName" v-loading.fullscreen.lock="fullscreenLoading">
		<el-tab-pane label="慢日志汇总" name="first">
			<el-row style="padding-bottom:20px">
				<span class="demonstration">时间范围</span>
				<!-- <el-date-picker size="small" v-model="time" type="datetimerange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd HH:mm:ss" :default-time="defaultTime"></el-date-picker> -->

				<el-date-picker size="small" v-model="time" type="datetimerange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd HH:mm:ss" :default-time="['00:00:00','23:59:59']"></el-date-picker>
				<!-- <el-select v-model="hostip" filterable placeholder="请选择数据库" size="small">
					<el-option v-for="item in options" :key="item" :label="item" :value="item"></el-option>
				</el-select> -->
				<el-button size="small" type="primary" icon="el-icon-search" v-on:click="get_slow_log()" round>查询</el-button>
			</el-row>
			
			<el-row>
				<el-table :data="detail_slow_logs.slice((currentPage-1)*pagesize,currentPage*pagesize)" border style="width: 100%">
					<el-table-column prop="start_time" label="start_time" width=180 sortable>
					</el-table-column>
					<el-table-column prop="query_time" label="query_time" width=100 sortable>
					</el-table-column>
					<el-table-column prop="rows_examined" label="rows_examined" width="100" sortable>
					</el-table-column>
					<el-table-column prop="rows_sent" label="rows_sent" width="100" sortable>
					</el-table-column>
					<el-table-column prop="db" label="db" width="80" sortable>
					</el-table-column>
					<el-table-column prop="user_host" label="user_host" width="200" >
					</el-table-column>
					<el-table-column prop="thread_id" label="thread_id" width="100" sortable>
					</el-table-column>
					<el-table-column prop="sql_text"  show-overflow-tooltip="true" label="sql_text" sortable>
					</el-table-column>
				</el-table>
				  <el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="currentPage"
    :page-sizes="[10, 20, 30, 40]"
    :page-size="pagesize"
    layout="total, sizes, prev, pager, next, jumper"
    :total="detail_slow_logs.length">
  </el-pagination>
			</el-row>
		</el-tab-pane>
			</div>
		</el-tab-pane>
	</el-tabs>
</template>
<script>

	export default {

		props: {},
		data() {
			return {
				fullscreenLoading: false,
				// time: '',
				time: [],
				currentPage:1, //初始页
                pagesize:10, // 每页的数据
				activeName: 'first',
				options:[],
				hostip: "",
				detail_slow_logs: [],
				loading: false,
				bar: {
					title: {
						text: '时间分布'
					},
					tooltip: {
						trigger: 'item',
						show: true,
						formatter: function(params) {
							return params;
						}
					},
					xAxis: {
						type: 'time',
						data: ['2019-04-28 00:00:00', '2019-04-29 00:00:00']
					},
					yAxis: {},
					series: [{
						symbolSize: 5,
						name: 'Sales',
						type: 'scatter',
						cursor: "pointer",
						data: []
					}]
				}
			};
		},
		created: function() {
			this.first_slow_log();
		},
		methods: {
		handleSizeChange: function (size) {
this.pagesize = size;
console.log(this.pagesize) //每页下拉显示数据
},
handleCurrentChange: function(currentPage){
this.currentPage = currentPage;
console.log(this.currentPage) //点击第几页
},
			doRandom() {
				alert('hello')
			},

			get_slow_log: function() {
				this.vip = this.$route.query.vip;
				console.log(this.time);
				this.fullscreenLoading = true;
				this.$http
					.post(
						"/api/mysql_log/get_slow_log/", {
							start_time: this.time[0],
							stop_time: this.time[1],
							vip: this.vip,
						},
					)
					.then(
						function(res) {
							if (res.data.status === false) {
								this.$message.error(res.data.msg);
							} else {
								this.$message.success(res.data.msg);
								this.fullscreenLoading = false;
								this.detail_slow_logs = res.data.data;
							}
						}.bind(this)
					)
					.catch(function(error) {
						console.log(error);
					});
			},

			first_slow_log: function() {
				this.vip = this.$route.query.vip;
				this.fullscreenLoading = true;
				this.$http
					.post(
						"/api/mysql_log/first_slow_log/", {
							vip: this.vip,
						},
					)
					.then(
						function(res) {
							if (res.data.status === false) {
								this.$message.error(res.data.msg);
							} else {
								this.$message.success(res.data.msg);
								this.fullscreenLoading = false;
								this.detail_slow_logs = res.data.data;
							}
						}.bind(this)
					)
					.catch(function(error) {
						console.log(error);
					});
			},
		}
	};
</script>
<style>
</style>

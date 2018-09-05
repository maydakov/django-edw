import React, { Component } from 'react';
import Entities from 'components/Entities';
import TermsTree from 'components/TermsTree';
import Paginator from 'components/Paginator';
import ViewComponents from 'components/ViewComponents';
import Ordering from 'components/Ordering';
import Limits from 'components/Limits';
import Statistics from 'components/Statistics';
import Aggregation from 'components/Aggregation';
import DataMartsList from 'components/DataMartsList';
import GroupTitle from 'components/GroupTitle';


export default class DataMart extends Component {
  render() {

    const { entry_point_id, entry_points, actions } = this.props;

    return (
      <div className="row">
        <div className="col-sm-12 col-md-12">
            {
              Object.keys(entry_points).length > 1 ? <DataMartsList
                entry_points={entry_points}
                entry_point_id={entry_point_id}
                actions={actions}
              /> : null
            }
        </div>
        <div className="col-sm-4 col-md-3 sidebar-filter">
          <TermsTree entry_points={entry_points} entry_point_id={entry_point_id} />
        </div>
        <div className="col-sm-8 col-md-9">
          <div className="row">
            <div className="col-sm-6 col-md-4 ex-view-as">
              <ViewComponents entry_points={entry_points} entry_point_id={entry_point_id} />
            </div>
            <div className="col-sm-6 col-md-4 ex-order-by ex-dropdown ex-state-closed">
              <Ordering entry_points={entry_points} entry_point_id={entry_point_id} />
            </div>
            <div className="col-sm-6 col-md-2 ex-howmany-items ex-dropdown ex-state-closed">
              <Limits entry_points={entry_points} entry_point_id={entry_point_id} />
            </div>
            <div className="col-sm-6 col-md-2 ex-statistic float-right">
              <Statistics entry_points={entry_points} entry_point_id={entry_point_id} />
            </div>
          </div>
          <div className="row">
            <GroupTitle/>
          </div>
          <Entities entry_points={entry_points} entry_point_id={entry_point_id} />
          <Paginator entry_points={entry_points} entry_point_id={entry_point_id} />
          <Aggregation entry_points={entry_points} entry_point_id={entry_point_id} />
        </div>
      </div>
    );
  }
}

# Django imports
from django.test import TestCase
from django.conf import settings

# Third party imports
from model_mommy import mommy

# Devilry imports
from devilry.devilry_group import devilry_group_mommy_factories as group_mommy
from devilry.devilry_group.feedbackfeed_builder.feedbackfeed_timelinebuilder import FeedbackFeedTimelineBuilder
from devilry.devilry_group.feedbackfeed_builder import builder_base
from devilry.devilry_dbcache.customsql import AssignmentGroupDbCacheCustomSql


class TestTimelineBuilder(TestCase):
    devilryrole = 'student'

    def setUp(self):
        AssignmentGroupDbCacheCustomSql().initialize()

    def __build_timeline(self, group, user, assignment):
        feedbackset_queryset = builder_base.get_feedbackfeed_builder_queryset(
            group=group,
            requestuser=user,
            devilryrole=self.devilryrole
        )
        timeline_builder = FeedbackFeedTimelineBuilder(
            assignment=assignment,
            feedbacksets=feedbackset_queryset,
            group=group
        )
        timeline_builder.build()
        timeline_list = timeline_builder.get_as_list()
        return timeline_list

    def test_one_feedbackset_unpublished_event(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_end')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_unpublished(group=testgroup)
        feedbackset_queryset = builder_base.get_feedbackfeed_builder_queryset(
            group=testgroup,
            requestuser=testuser,
            devilryrole=self.devilryrole
        )
        timeline_builder = FeedbackFeedTimelineBuilder(
            assignment=testassignment,
            feedbacksets=feedbackset_queryset,
            group=testgroup
        )
        timeline_builder.build()
        timeline_list = timeline_builder.get_as_list()
        self.assertEquals(len(timeline_list), 1)
        self.assertEquals(timeline_list[0]['feedbackset_events'], [])

    def test_one_feedbackset_published_event(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_end')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        testfeedbackset = group_mommy.feedbackset_first_attempt_published(group=testgroup)
        feedbackset_queryset = builder_base.get_feedbackfeed_builder_queryset(
            group=testgroup,
            requestuser=testuser,
            devilryrole=self.devilryrole
        )
        timeline_builder = FeedbackFeedTimelineBuilder(
            assignment=testassignment,
            feedbacksets=feedbackset_queryset,
            group=testgroup
        )
        timeline_builder.build()
        timeline_list = timeline_builder.get_as_list()
        self.assertEquals(len(timeline_list), 1)
        self.assertEquals(timeline_list[0]['feedbackset_events'][0]['type'], 'grade')
        self.assertEquals(timeline_list[0]['feedbackset_events'][0]['grade_points'], testfeedbackset.grading_points)

    def test_feedbackset_published_grading_points_same_as_first_updated_grading_points(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_end')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        testfeedbackset = group_mommy.feedbackset_first_attempt_published(group=testgroup)
        first_grading_points_update = mommy.make('devilry_group.FeedbackSetGradingUpdateHistory',
                                                 old_grading_points=testfeedbackset.grading_points,
                                                 feedback_set=testfeedbackset)
        last_grading_points_update = mommy.make('devilry_group.FeedbackSetGradingUpdateHistory',
                                                old_grading_points=0,
                                                feedback_set=testfeedbackset)
        feedbackset_queryset = builder_base.get_feedbackfeed_builder_queryset(
            group=testgroup,
            requestuser=testuser,
            devilryrole=self.devilryrole
        )
        timeline_builder = FeedbackFeedTimelineBuilder(
            assignment=testassignment,
            feedbacksets=feedbackset_queryset,
            group=testgroup
        )
        timeline_builder.build()
        timeline_list = timeline_builder.get_as_list()
        self.assertEquals(len(timeline_list), 1)
        self.assertEquals(timeline_list[0]['feedbackset_events'][0]['type'], 'grade')
        self.assertEquals(timeline_list[0]['feedbackset_events'][0]['grade_points'],
                             first_grading_points_update.old_grading_points)
        self.assertNotEquals(timeline_list[0]['feedbackset_events'][0]['grade_points'],
                          last_grading_points_update.old_grading_points)

    def test_updated_grading_points_event_no_updates(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_end')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        timeline_list = self.__build_timeline(group=testgroup, user=testuser, assignment=testassignment)
        self.assertEqual(len(timeline_list[0]['feedbackset_events']), 1)

    def test_updated_grading_points_event_one_update(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_end')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        testfeedbackset = group_mommy.feedbackset_first_attempt_published(group=testgroup)
        mommy.make('devilry_group.FeedbackSetGradingUpdateHistory',
                   old_grading_points=testfeedbackset.grading_points,
                   feedback_set=testfeedbackset)
        timeline_list = self.__build_timeline(group=testgroup, user=testuser, assignment=testassignment)
        self.assertEqual(len(timeline_list[0]['feedbackset_events']), 2)
        self.assertEqual(timeline_list[0]['feedbackset_events'][0]['type'], 'grade')
        self.assertEqual(timeline_list[0]['feedbackset_events'][1]['type'], 'grading_updated')
        self.assertEqual(timeline_list[0]['feedbackset_events'][1]['obj'].old_grading_points,
                         testfeedbackset.grading_points)

    def test_updated_grading_points_event_multiple_updates(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_end')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        testfeedbackset = group_mommy.feedbackset_first_attempt_published(group=testgroup, grading_points=1)
        mommy.make('devilry_group.FeedbackSetGradingUpdateHistory',
                   old_grading_points=testfeedbackset.grading_points,
                   feedback_set=testfeedbackset)
        mommy.make('devilry_group.FeedbackSetGradingUpdateHistory',
                   old_grading_points=0,
                   feedback_set=testfeedbackset)
        mommy.make('devilry_group.FeedbackSetGradingUpdateHistory',
                   old_grading_points=1,
                   feedback_set=testfeedbackset)
        timeline_list = self.__build_timeline(group=testgroup, user=testuser, assignment=testassignment)
        self.assertEqual(len(timeline_list[0]['feedbackset_events']), 4)
        self.assertEqual(timeline_list[0]['feedbackset_events'][0]['type'], 'grade')
        self.assertEqual(timeline_list[0]['feedbackset_events'][1]['type'], 'grading_updated')
        self.assertEqual(timeline_list[0]['feedbackset_events'][1]['obj'].old_grading_points, 1)
        self.assertEqual(timeline_list[0]['feedbackset_events'][1]['next_grading_points'], 0)
        self.assertEqual(timeline_list[0]['feedbackset_events'][2]['obj'].old_grading_points, 0)
        self.assertEqual(timeline_list[0]['feedbackset_events'][2]['next_grading_points'], 1)
        self.assertEqual(timeline_list[0]['feedbackset_events'][3]['obj'].old_grading_points, 1)
        self.assertEqual(timeline_list[0]['feedbackset_events'][3]['next_grading_points'], 1)


class TestTimelineBuilderExaminer(TestTimelineBuilder):
    devilryrole = 'examiner'


class TestTimelineBuilderAdmin(TestTimelineBuilder):
    devilryrole = 'admin'



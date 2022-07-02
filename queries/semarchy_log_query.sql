-- Query to return logging details in Semarchy xDM (and Semarchy Convergence for MDM 3.x)
-- This query returns details of an integration batch for a specified Batch ID.
-- Note the single bind variable: :BATCHID
-- SQL*Developer prompts for a bound variable value when you execute this query.
-- pgAdmin4 and other tools do not support bind variables, so you must edit the query before executing:
--   Replace ":BATCHID" in line 41 with your specified batchid

with LOGS as (
    select
        BATCHID
        ,JI.NAME JOB_INSTANCE_NAME
        ,JL.START_DATE JOB_START_DATE
        ,JL.END_DATE JOB_END_DATE
        ,JL.ROW_COUNT JOB_ROW_COUNT
        ,JL.ERR_COUNT JOB_REJECTS_COUNT
        ,JL.STATUS JOB_STATUS /* RUNNING, DONE, WARNING, ERROR */
        ,JL.MESSAGE JOB_MESSAGE
        ,TL1.NAME TASK_NAME1
        ,TL2.NAME TASK_NAME2
        ,TL3.NAME TASK_NAME3
        ,TL4.NAME TASK_NAME4
        ,TL1.MESSAGE TASK_MESSAGE1
        ,coalesce(TL4.ROW_COUNT, TL3.ROW_COUNT, TL2.ROW_COUNT, TL1.ROW_COUNT) TASK_ROW_COUNT
        ,coalesce(TL4.START_DATE, TL3.START_DATE, TL2.START_DATE, TL1.START_DATE) TASK_START_DATE
        ,coalesce(TL4.END_DATE, TL3.END_DATE, TL2.END_DATE, TL1.END_DATE) TASK_END_DATE
        ,coalesce(TL4.STATUS, TL3.STATUS, TL2.STATUS, TL1.STATUS) TASK_STATUS
        ,coalesce(TL4.MESSAGE, TL3.MESSAGE, TL2.MESSAGE, TL1.MESSAGE) TASK_MESSAGE
        ,coalesce(TD4.SQL, TD3.SQL, TD2.SQL, TD1.SQL) TASK_SQL
    from
      SEMARCHY_REPOSITORY.dbo.MTA_INTEG_BATCH B
        inner join SEMARCHY_REPOSITORY.dbo.MTA_JOB_INSTANCE JI on ( B.R_JOBINSTANCE = JI.UUID)
        inner join SEMARCHY_REPOSITORY.dbo.MTA_JOB_LOG JL on ( JI.UUID = JL.R_JOBINSTANCE)
        inner join SEMARCHY_REPOSITORY.dbo.MTA_TASK_LOG TL1 on ( JL.UUID = TL1.O_JOBLOG and TL1.R_TASKLOG is null)
        left join SEMARCHY_REPOSITORY.dbo.MTA_TASK_LOG TL2 on ( TL1.UUID = TL2.R_TASKLOG )
        left join SEMARCHY_REPOSITORY.dbo.MTA_TASK_LOG TL3 on ( TL2.UUID = TL3.R_TASKLOG )
        left join SEMARCHY_REPOSITORY.dbo.MTA_TASK_LOG TL4 on ( TL3.UUID = TL4.R_TASKLOG )
        left join SEMARCHY_REPOSITORY.dbo.MTA_TASK_DEF TD1 on ( TD1.UUID = TL1.R_TASKDEF )
        left join SEMARCHY_REPOSITORY.dbo.MTA_TASK_DEF TD2 on ( TD2.UUID = TL2.R_TASKDEF )
        left join SEMARCHY_REPOSITORY.dbo.MTA_TASK_DEF TD3 on ( TD3.UUID = TL3.R_TASKDEF )
        left join SEMARCHY_REPOSITORY.dbo.MTA_TASK_DEF TD4 on ( TD4.UUID = TL4.R_TASKDEF )
    where B.BATCHID = :BATCHID /* SQLDeveloper will prompt for a batch ID. In other tools, replace :BATCHID with your batch ID before executing. */
)

select
    BATCHID, JOB_INSTANCE_NAME, JOB_START_DATE, JOB_END_DATE,
    JOB_ROW_COUNT, JOB_REJECTS_COUNT, JOB_STATUS, JOB_MESSAGE,
    TASK_NAME1, TASK_NAME2, TASK_NAME3, TASK_NAME4,
    TASK_ROW_COUNT, TASK_START_DATE, TASK_END_DATE,
  datediff(s, TASK_START_DATE, TASK_END_DATE) DUR_SEC,
    TASK_STATUS,
    TASK_MESSAGE,
    TASK_SQL
from LOGS
order by TASK_START_DATE ;
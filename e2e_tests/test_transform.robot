# -*- coding: robot -*-

*** Settings ***
Library           OperatingSystem
Library           Collections
Library           Process
Library           DateTime

*** Variables ***
${HOST}   localhost
${UDP_URI}   udp://localhost:6002
${RTSP_URI}     rtsp://localhost:1235/file2.rtsp
${FFSERVER}   ffserver -f ffserver.config
${UDP_BROADCAST}     gst-launch-1.0 -v filesrc location=SampleVideo_1280x720_5mb.mp4 ! decodebin ! x264enc ! rtph264pay ! udpsink host=localhost port=6002
${TEST_RUN}     transform -u ${UDP_URI} -n 2000

*** Test Cases ***
Start Udp Broadcast
    [Documentation]   Launch gstreamer
    [Tags]    gstreamer
    ${CMD_RES}=    Start Process    ${UDP_BROADCAST}    shell=True	stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    #Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}

Set Up Dir    
    ${OUT_DIR}=    Create Out Dir
    Set Global Variable      ${OUT_DIR}

Transform Udp Mp4
    [Documentation]   Run python script
    [Tags]    python
    ${CMD_RES}=    Run Process    ${TEST_RUN} -o mp4 -d ${OUT_DIR}/out.mp4   shell=True	timeout=3min  stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}
    Should Be Equal As Integers   ${CMD_RES.rc}   0

Transform Udp Frames
    [Documentation]   Run python script
    [Tags]    python
    ${CMD_RES}=    Run Process    ${TEST_RUN} -o frame -d ${OUT_DIR}/out%00d.jpg   shell=True	timeout=3min  stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}
    Should Be Equal As Integers   ${CMD_RES.rc}   0

Stop Udp Broadcast
    Terminate All Processes

*** Keywords ***
Create Out Dir
    ${TD}=    Get Current Date    result_format=%Y-%m-%d--%H-%M-%S
    Create Directory    out_${TD}
    [return]    out_${TD}
from easydict import EasyDict

import torch
torch.cuda.set_device(0)
# ==== NOTE: 需要设置cfg_atari中的action_shape =====

# options={'PongNoFrameskip-v4', 'QbertNoFrameskip-v4', 'MsPacmanNoFrameskip-v4', 'SpaceInvadersNoFrameskip-v4', 'BreakoutNoFrameskip-v4', ...}
env_name = 'PongNoFrameskip-v4'
# env_name = 'MsPacmanNoFrameskip-v4'
# env_name = 'QbertNoFrameskip-v4'
# env_name = 'SeaquestNoFrameskip-v4'
# env_name = 'BoxingNoFrameskip-v4'
# env_name = 'FrostbiteNoFrameskip-v4'
# env_name = 'BreakoutNoFrameskip-v4'  # TODO: eval_sample, episode_steps


if env_name == 'PongNoFrameskip-v4':
    action_space_size = 6
    # action_space_size = 18
    update_per_collect = None # for others
elif env_name == 'QbertNoFrameskip-v4':
    action_space_size = 6
    update_per_collect = None # for others
elif env_name == 'MsPacmanNoFrameskip-v4':
    action_space_size = 9
    update_per_collect = None # for others
elif env_name == 'SpaceInvadersNoFrameskip-v4':
    action_space_size = 6
    update_per_collect = None # for others
elif env_name == 'BreakoutNoFrameskip-v4':
    action_space_size = 4
    update_per_collect = None # for others
elif env_name == 'SeaquestNoFrameskip-v4':
    action_space_size = 18
    update_per_collect = None # for others
elif env_name == 'BoxingNoFrameskip-v4':
    action_space_size = 18
    update_per_collect = None # for others
elif env_name == 'FrostbiteNoFrameskip-v4':
    action_space_size = 18
    update_per_collect = None # for others

# ==============================================================
# begin of the most frequently changed config specified by the user
# ==============================================================
# collector_env_num = 8
# n_episode = 8
collector_env_num  = 1 # TODO
n_episode = 1
evaluator_env_num = 3

model_update_ratio = 0.25
num_simulations = 50
# max_env_step = int(1e6)
max_env_step = int(5e5)

reanalyze_ratio = 0. 
# reanalyze_ratio = 0.05 # TODO

# batch_size = 64
batch_size = 8

# num_unroll_steps = 5
num_unroll_steps = 10
# num_unroll_steps = 20 # TODO
# num_unroll_steps = 30 # TODO
# num_unroll_steps = 40 # TODO


threshold_training_steps_for_final_temperature = int(5e4)  # train_iter 50k 1->0.5->0.25
# eps_greedy_exploration_in_collect = True # for breakout, qbert, boxing
eps_greedy_exploration_in_collect = False 
# ==============================================================
# end of the most frequently changed config specified by the user
# ==============================================================

atari_unizero_config = dict(
    # TODO: 
    # mcts_ctree
    # muzero_collector/evaluator: empty_cache
    exp_name=f'data_paper_muzero_visualize/{env_name[:-14]}/{env_name[:-14]}_unizero_upc{update_per_collect}-mur{model_update_ratio}_H{num_unroll_steps}_bs{batch_size}_stack1_conlen{8}_lsd768-nlayer4-nh8_bacth-kvmaxsize_seed0',
    # exp_name=f'data_paper_ablation_0429/{env_name[:-14]}/{env_name[:-14]}_unizero_upc{update_per_collect}-mur{model_update_ratio}_H{num_unroll_steps}_bs{batch_size}_stack1_conlen{8}_lsd768-nlayer4-nh8_bacth-kvmaxsize_seed0',
    # exp_name=f'data_paper_learn-dynamics_0423/{env_name[:-14]}_unizero_upc{update_per_collect}-mur{model_update_ratio}_H{num_unroll_steps}_bs{batch_size}_stack1_conlen{8}_lsd768-nlayer1-nh8_bacth-kvmaxsize_analysis_dratio0025_seed0',
    # exp_name=f'data_paper_learn-dynamics_0422/{env_name[:-14]}_unizero_upc{update_per_collect}-mur{model_update_ratio}_H{num_unroll_steps}_bs{batch_size}_stack1_conlen{8}_lsd768-nlayer1-nh8_bacth-kvmaxsize_seed0',
    # exp_name=f'data_paper_learn-dynamics_0422/{env_name[:-14]}_unizero_envnum{collector_env_num}_ns{num_simulations}_upc{update_per_collect}-mur{model_update_ratio}_rr{reanalyze_ratio}_H{num_unroll_steps}_bs{batch_size}_stack1_grugating-false_latent-groupkl_conleninit{8}-conlenrecur{8}clear_lsd768-nlayer1-nh8_bacth-kvmaxsize-fix0417_seed0',

    env=dict(
        stop_value=int(1e6),
        env_name=env_name,
        observation_shape=(3, 64, 64),
        gray_scale=False,
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
        n_evaluator_episode=evaluator_env_num,
        manager=dict(shared_memory=False, ),
        # TODO: debug
        # collect_max_episode_steps=int(50),
        # eval_max_episode_steps=int(50),
        # TODO: for breakout
        # collect_max_episode_steps=int(5e3), # for breakout
        # eval_max_episode_steps=int(5e3), # for breakout
        # TODO: for others
        collect_max_episode_steps=int(2e4), 
        eval_max_episode_steps=int(1e4),
        clip_rewards=True,
    ),
    policy=dict(
        analysis_sim_norm=False, # TODO
        cal_dormant_ratio=False, # TODO
        learn=dict(
            learner=dict(
                hook=dict(
                    load_ckpt_before_run='',
                    log_show_after_iter=100,
                    save_ckpt_after_iter=200000,  # default is 1000
                    save_ckpt_after_run=True,
                ),
            ),
        ),
        # model_path=None,
        model_path='/mnt/afs/niuyazhe/code/LightZero/data_unizero_paper/data_paper_unizero_atari-20-games_0424/Pong_unizero_upcNone-mur0.25_H10_bs64_stack1_conlen8_lsd768-nlayer1-nh8_bacth-kvmaxsize_seed0/ckpt/ckpt_best.pth.tar',
        tokenizer_start_after_envsteps=int(0),
        transformer_start_after_envsteps=int(0),
        update_per_collect_transformer=update_per_collect,
        update_per_collect_tokenizer=update_per_collect,
        num_unroll_steps=num_unroll_steps,
        model=dict(
            analysis_sim_norm = False,
            observation_shape=(3, 64, 64),
            image_channel=3,
            frame_stack_num=1,
            gray_scale=False,
            action_space_size=action_space_size,
            downsample=True,
            self_supervised_learning_loss=True,  # default is False
            discrete_action_encoding_type='one_hot',
            norm_type='BN',
            # reward_support_size=601,
            # value_support_size=601,
            # support_scale=300,
            reward_support_size=101,
            value_support_size=101,
            support_scale=50,
        ),
        use_priority=False, # TODO
        use_augmentation=False,  # TODO
        # use_augmentation=True,  # NOTE: only for image-based atari
        cuda=True,
        env_type='not_board_games',
        game_segment_length=400,
        random_collect_episode_num=0,
        eps=dict(
            eps_greedy_exploration_in_collect=eps_greedy_exploration_in_collect,
            # need to dynamically adjust the number of decay steps 
            # according to the characteristics of the environment and the algorithm
            type='linear',
            start=1.,
            end=0.01,
            decay=int(2e4),  # TODO: 20k
        ),
        update_per_collect=update_per_collect,
        model_update_ratio = model_update_ratio,
        batch_size=batch_size,
        # manual_temperature_decay=True,
        # threshold_training_steps_for_final_temperature=threshold_training_steps_for_final_temperature,
        optim_type='AdamW',
        lr_piecewise_constant_decay=False,
        learning_rate=0.0001,
        target_update_freq=100,
        # grad_clip_value = 0.5, # TODO: 1
        grad_clip_value = 5, # TODO: 1
        num_simulations=num_simulations,
        reanalyze_ratio=reanalyze_ratio,
        n_episode=n_episode,
        # eval_freq=int(9e9),
        # eval_freq=int(1e4),
        eval_freq=int(2e3),
        replay_buffer_size=int(1e6),  # the size/capacity of replay_buffer, in the terms of transitions.
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
    ),
)
atari_unizero_config = EasyDict(atari_unizero_config)
main_config = atari_unizero_config

atari_unizero_create_config = dict(
    env=dict(
        type='atari_lightzero',
        import_names=['zoo.atari.envs.atari_lightzero_env'],
    ),
    env_manager=dict(type='subprocess'),
    policy=dict(
        type='unizero',
        import_names=['lzero.policy.unizero'],
    ),
)
atari_unizero_create_config = EasyDict(atari_unizero_create_config)
create_config = atari_unizero_create_config

if __name__ == "__main__":
    # max_env_step = 10000
    from lzero.entry import train_unizero
    train_unizero([main_config, create_config], seed=0, model_path=main_config.policy.model_path, max_env_step=max_env_step)



    # 下面为cprofile的代码
    # from lzero.entry import train_unizero
    # def run(max_env_step: int):
    #     train_unizero([main_config, create_config], seed=0, model_path=main_config.policy.model_path, max_env_step=max_env_step)
    # import cProfile
    # cProfile.run(f"run({100000})", filename="pong_unizero_cprofile_100k_envstep", sort="cumulative")

    # python -m line_profiler  /mnt/afs/niuyazhe/code/LightZero/atari_unizero_config_stack1.py.lprof >  atari_unizero_config_stack1.py.lprof.txt